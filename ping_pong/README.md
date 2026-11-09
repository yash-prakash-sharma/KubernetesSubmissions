# Ping-pong

Responds to GET /pingpong with "pong N", where N is a counter that increases
on each request. The counter is in memory and resets when the pod restarts.
The port is set with the PORT environment variable (default 3000).

## Build the image (optional)
    docker build -t YOUR_DOCKERHUB_USER/ping-pong:1.9 .
    docker push YOUR_DOCKERHUB_USER/ping-pong:1.9

## Deploy

    k3d cluster create -p 8081:80@loadbalancer -a 2
    kubectl apply -f manifests/

## Use
    curl localhost:8081/pingpong