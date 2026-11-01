import os
from http.server import BaseHTTPRequestHandler, HTTPServer\

PORT = int(os.environ.get("PORT", 8000))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Todo app\n")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Server started in port {PORT}", flush=True)
    server.serve_forever()