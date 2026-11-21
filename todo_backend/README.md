# Todo backend

Stores todos in memory and exposes:
- GET /todos: returns a JSON list of todos
- POST /todos: creates a todo from JSON like {"todo": "text"} (1-140 characters, otherwise 400)

The port is set with the PORT environment variable (default 3000).
Data is lost when the pod restarts, and the deployment must stay at one replica.

## Build the image (optional)
    docker build -t yashprakashsharma/todo-backend:2.2 .
    docker push yashprakashsharma/todo-backend:2.2

## Deploy
    kubectl apply -f manifests/
The Ingress that routes /todos to this service is in ../todo_app/manifests/ingress.yaml.

## Use
    curl localhost:8081/todos
    curl localhost:8081/todos -X POST -H "Content-Type: application/json" -d '{"todo":"Buy milk"}' localhost:8081/todos