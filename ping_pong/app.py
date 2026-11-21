import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", 3000))

counter = 0
lock = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        global counter
        if self.path == "/pingpong":
            with lock:
                body = f"pong {counter}\n".encode()
                counter += 1
            self.respond(200, body)
        elif self.path == "/pings":
            with lock:
                body = f"{counter}\n".encode()
            self.respond(200, body)
        else:
            self.respond(404, b"Not found\n")


if __name__ == "__main__":
    print(f"Server started in port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()