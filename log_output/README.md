# Log output

Generates a random UUID at startup and prints it with a timestamp every 5 seconds.
It also serves the current timestamp and the random string over HTTP, exposed
through an Ingress.

The port is set with the `PORT` environment variable (default 3000).

## Cluster setup

The Ingress needs a port mapping on the cluster:

    k3d cluster create -p 8081:80@loadbalancer -a 2

## Build the image (optional)

    docker build -t YOUR_DOCKERHUB_USER/hash-app:1.7 .
    docker push YOUR_DOCKERHUB_USER/hash-app:1.7

## Deploy

    kubectl apply -f manifests/
    kubectl logs -f deployment/hashgenerator-deployment

## Use

Open http://localhost:8081 in a browser (or run `curl localhost:8081`).
It returns the current timestamp and the random string, which stays the same
as long as the pod runs.