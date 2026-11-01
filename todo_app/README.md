# Todo app

A small web server that prints "Server started in port NNNN" on startup.
The port is set with the PORT environment variable (default 8000).

## Run
    # To create your custom image for application
    docker build -t YOUR_DOCKERHUB_USER/ltodo-app:1.2 .
    docker push YOUR_DOCKERHUB_USER/todo-app:1.2

    # To run existing application
    kubectl apply -f manifests/deployment.yaml
    kubectl logs -f deployment/todoapp-deployment
    kubectl port-forward todoapp-deployment-xxxxxxxxxx-xxxxx 3003:3000

## Access
    Replace the pod name with yours. The format is LOCAL_PORT:CONTAINER_PORT, so 3003 on your laptop goes to 3000 in the pod. Leave that terminal running and open http://localhost:3003 in your browser. You should see your page
    