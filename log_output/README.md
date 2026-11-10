## Structure
The pod has two containers sharing an emptyDir volume mounted at /shared:
- writer: generates a random string on startup and writes the timestamp and string to /shared/log.txt every 5 seconds
- reader: serves the contents of that file on GET /

## Build the images (optional)
    docker build -t YOUR_DOCKERHUB_USER/log-output-writer:1.10 writer
    docker build -t YOUR_DOCKERHUB_USER/log-output-reader:1.10 reader

## Deploy
    kubectl apply -f manifests/
    kubectl logs -f deployment/log-output-dep -c writer

## Use
    curl localhost:8081/