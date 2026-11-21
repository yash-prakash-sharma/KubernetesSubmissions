import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", 3000))
MAX_LEN = 140

todos = ["Learn JavaScript", "Learn React", "Build a project"]
lock = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/todos":
            with lock:
                self.send_json(200, list(todos))
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/todos":
            self.send_json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
            todo = payload["todo"]
            if not isinstance(todo, str):
                raise ValueError("todo must be a string")
        except (ValueError, KeyError, TypeError):
            self.send_json(400, {"error": "body must be JSON like {\"todo\": \"text\"}"})
            return
        todo = todo.strip()
        if not todo or len(todo) > MAX_LEN:
            self.send_json(400, {"error": f"todo must be 1-{MAX_LEN} characters"})
            return
        with lock:
            todos.append(todo)
        print(f"Added todo: {todo}", flush=True)
        self.send_json(201, {"todo": todo})


if __name__ == "__main__":
    print(f"Server started in port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()