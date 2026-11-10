import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", 3000))
FILE = os.environ.get("LOG_FILE", "/shared/log.txt")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            return
        try:
            with open(FILE, "rb") as f:
                body = f.read()
            status = 200
        except FileNotFoundError:
            body = b"No log file yet, try again in a few seconds\n"
            status = 503
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"Server started in port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()