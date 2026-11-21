import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", 3000))
LOG_FILE = os.environ.get("LOG_FILE", "/shared/log.txt")
PONG_FILE = os.environ.get("PONG_FILE", "/data/pingpongs.txt")


def last_line(path):
    try:
        with open(path) as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines[-1] if lines else None
    except FileNotFoundError:
        return None


def read_pongs():
    try:
        with open(PONG_FILE) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            return
        line = last_line(LOG_FILE)
        if line is None:
            status, body = 503, b"No log line yet, try again in a few seconds\n"
        else:
            status = 200
            body = f"{line}.\nPing / Pongs: {read_pongs()}\n".encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"Server started in port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()