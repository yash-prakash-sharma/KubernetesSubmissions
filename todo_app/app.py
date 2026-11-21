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

HTML = b"""<!DOCTYPE html>
<html>
  <head><meta charset="utf-8"><title>Todo app</title></head>
  <body style="font-family: sans-serif; max-width: 600px; margin: 2rem auto;">
    <h1>Todo app</h1>
    <img src="/image" alt="Random picture" width="400">
    <p>The picture changes every 10 minutes.</p>
    <h2>Todos</h2>
    <ul>
      <li>Learn JavaScript</li>
      <li>Learn React</li>
      <li>Build a project</li>
    </ul>
  </body>
</html>
"""


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
            fetch_image()  # first run: nothing cached yet
        elif time.time() - meta["fetched_at"] >= MAX_AGE:
            if not meta["stale_served"]:
                # expired: serve the old picture one more time
                meta["stale_served"] = True
                write_meta(meta)
            else:
                # the next request after that gets a fresh picture
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