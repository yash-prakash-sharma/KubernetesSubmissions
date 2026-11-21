## Structure
The pod has two containers sharing an emptyDir volume mounted at /shared:
- writer: generates a random string on startup and writes the timestamp and string to /shared/log.txt every 5 seconds
- reader: serves the contents of that file on GET /


## Output
GET / returns the latest timestamp and random string, then the number of
ping-pong requests:

    2026-11-21T07:30:12.345Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43.
    Ping / Pongs: 3

The reader container reads the count from `/data/pingpongs.txt`, written by the
ping-pong application, through the shared persistent volume (see ../persistentvolume).

## Build the reader image (optional)
    docker build -t YOUR_DOCKERHUB_USER/log-output-reader:1.11 reader

## Deploy order
    kubectl apply -f ../persistentvolume/
    kubectl apply -f ../ping_pong/manifests/
    kubectl apply -f manifests/

## Use
    curl localhost:8081/