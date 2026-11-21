import json
import os
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", 3000))
IMAGE_DIR = os.environ.get("IMAGE_DIR", "/data/image")
IMAGE_URL = os.environ.get("IMAGE_URL", "https://picsum.photos/1200")
MAX_AGE = int(os.environ.get("IMAGE_MAX_AGE", 600))  # seconds
ENABLE_SHUTDOWN = os.environ.get("ENABLE_SHUTDOWN", "false").lower() == "true"

IMAGE_FILE = os.path.join(IMAGE_DIR, "image.jpg")
META_FILE = os.path.join(IMAGE_DIR, "meta.json")

lock = threading.Lock()
os.makedirs(IMAGE_DIR, exist_ok=True)

HTML = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Todo app</title>
    <style>
      body { font-family: sans-serif; max-width: 600px; margin: 2rem auto; padding: 0 1rem; }
      img { width: 100%; max-width: 400px; display: block; margin-bottom: 1rem; }
      form { display: flex; gap: 0.5rem; }
      input[type=text] { flex: 1; padding: 0.5rem; }
      button { padding: 0.5rem 1rem; }
      #count { color: #666; font-size: 0.85rem; margin-top: 0.25rem; }
      #error { color: #b00020; margin-top: 0.5rem; }
    </style>
  </head>
  <body>
    <h1>Todo app</h1>
    <img src="/image" alt="Random picture">
    <p>The picture changes every 10 minutes.</p>

    <form id="todo-form">
      <input type="text" id="todo" maxlength="140" placeholder="What needs to be done?" autocomplete="off">
      <button type="submit">Send</button>
    </form>
    <div id="count">0 / 140</div>
    <div id="error"></div>

    <h2>Todos</h2>
    <ul id="todos"></ul>

    <script>
      const form = document.getElementById("todo-form");
      const input = document.getElementById("todo");
      const count = document.getElementById("count");
      const error = document.getElementById("error");
      const list = document.getElementById("todos");

      async function loadTodos() {
        try {
          const res = await fetch("/todos");
          if (!res.ok) throw new Error("status " + res.status);
          const todos = await res.json();
          list.replaceChildren(...todos.map((t) => {
            const li = document.createElement("li");
            li.textContent = t;
            return li;
          }));
        } catch (e) {
          error.textContent = "Could not load todos";
        }
      }

      input.addEventListener("input", () => {
        count.textContent = input.value.length + " / 140";
      });

      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        error.textContent = "";
        try {
          const res = await fetch("/todos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ todo: text }),
          });
          if (!res.ok) throw new Error("status " + res.status);
          input.value = "";
          count.textContent = "0 / 140";
          await loadTodos();
        } catch (e) {
          error.textContent = "Could not add the todo";
        }
      });

      loadTodos();
    </script>
  </body>
</html>
""".encode("utf-8")


def read_meta():
    try:
        with open(META_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, ValueError):
        return None


def write_meta(meta):
    tmp = META_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(meta, f)
    os.replace(tmp, META_FILE)


def fetch_image():
    req = urllib.request.Request(IMAGE_URL, headers={"User-Agent": "todo-app/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
    tmp = IMAGE_FILE + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, IMAGE_FILE)
    write_meta({"fetched_at": time.time(), "stale_served": False})
    print("Fetched a new image", flush=True)


def get_image():
    with lock:
        meta = read_meta()
        if meta is None or not os.path.exists(IMAGE_FILE):
            fetch_image()
        elif time.time() - meta["fetched_at"] >= MAX_AGE:
            if not meta["stale_served"]:
                meta["stale_served"] = True
                write_meta(meta)
            else:
                try:
                    fetch_image()
                except Exception as e:
                    print(f"Fetch failed, keeping old image: {e}", flush=True)
        with open(IMAGE_FILE, "rb") as f:
            return f.read()


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.respond(200, "text/html; charset=utf-8", HTML)
        elif self.path == "/image":
            try:
                self.respond(200, "image/jpeg", get_image())
            except Exception as e:
                print(f"Could not get image: {e}", flush=True)
                self.respond(502, "text/plain", b"Could not get an image\n")
        elif self.path == "/shutdown" and ENABLE_SHUTDOWN:
            self.respond(200, "text/plain", b"Shutting down\n")
            threading.Timer(0.5, lambda: os._exit(1)).start()
        else:
            self.respond(404, "text/plain", b"Not found\n")


if __name__ == "__main__":
    print(f"Server started in port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()