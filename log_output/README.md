### Structure
The pod has two containers sharing an emptyDir volume mounted at /shared:
- writer: writes a timestamp and random string to /shared/log.txt every 5 seconds
- reader: serves GET /, combining the latest log line with the ping-pong count

The count is fetched over HTTP from the ping-pong service
(PING_PONG_URL, default http://ping-pong-svc:1234/pings).
If ping-pong can't be reached it shows "unavailable".

## Output
    2026-11-21T12:45:17.705Z: 8523ecb1-c716-4cb6-a044-b9e83bb98e43.
    Ping / Pongs: 3

## Build the reader image (optional)
    docker build -t yashprakashsharma/log-output-reader:2.1 reader

## Deploy
    kubectl apply -f ../ping_pong/manifests/
    kubectl apply -f manifests/

## Use
    curl localhost:8081/