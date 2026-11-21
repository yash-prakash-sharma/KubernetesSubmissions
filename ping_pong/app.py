import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DATA_FILE = os.environ.get("DATA_FILE", "/data/pingpongs.txt")
PORT = int(os.environ.get("PORT", 8000))

lock = threading.Lock()

def load_counter():
    try:
        with open(DATA_FILE) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_counter(value):
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w") as f:
        f.write(str(value))
    os.replace(tmp, DATA_FILE)

os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
counter = load_counter()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global counter
        if self.path == "/pingpong":
            with lock:
                body = f"pong {counter}\n".encode()
                counter += 1
                save_counter(counter)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    print(f"Server started in port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()