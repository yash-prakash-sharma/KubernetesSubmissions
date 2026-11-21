## Todo UI
The page has a text input (max 140 characters, with a character counter),
todos are loaded from and sent to the todo-backend service through /todos.

## Cluster setup

The Ingress needs a port mapping on the cluster:

    k3d cluster create -p 8081:80@loadbalancer -a 2

## Picture
The page shows a random picture from https://picsum.photos, cached on the
persistent volume in `/data/image` (see ../persistentvolume). It is replaced
every 10 minutes: after expiry the old picture is served once more, and the
next request fetches a new one. Cached files survive container crashes.

## Configuration (environment variables)
- PORT: server port (default 8000)
- IMAGE_DIR: where the image is cached (default /data/image)
- IMAGE_MAX_AGE: seconds before the image expires (default 600)
- ENABLE_SHUTDOWN: if "true", GET /shutdown stops the process (for testing only)

## Deploy
# To create your custom image for application
    docker build -t YOUR_DOCKERHUB_USER/todo-app:2.2 .
    docker push YOUR_DOCKERHUB_USER/todo-app:2.2

Requires the persistent volume to be set up first.

    kubectl apply -f ../persistentvolume/
    kubectl apply -f ../todo_backend/manifests/
    kubectl apply -f manifests/

## Use
Open http://localhost:8081 (the cluster must be created with
`k3d cluster create -p 8081:80@loadbalancer -a 2`).

Open http://localhost:8081 . To test a crash: `curl localhost:8081/shutdown`.