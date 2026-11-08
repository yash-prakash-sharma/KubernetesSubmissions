import uuid
import time
import os
import threading
from datetime import timezone, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", 3000))
random_string = str(uuid.uuid4())


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def log_loop():
    while True:
        print(f"{now()}: {random_string}", flush=True)
        time.sleep(5)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/status"):
            body = f"{now()}: {random_string}\n".encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    threading.Thread(target=log_loop, daemon=True).start()
    print(f"Server started in port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()