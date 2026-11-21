# Ping-pong

- GET /pingpong: responds with "pong N" and increases the counter
- GET /pings: returns the number of requests so far (used by log-output over HTTP)

The counter is in memory and resets when the pod restarts.
The port is set with the PORT environment variable (default 3000).

## Build the image (optional)
    docker build -t yashprakashsharma/ping-pong:2.1 .
    docker push yashprakashsharma/ping-pong:2.1

## Deploy
    kubectl apply -f manifests/

The Ingress that routes /pingpong is in ../log_output/manifests/ingress.yaml.

## Use
    curl localhost:8081/pingpong