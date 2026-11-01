# Log output

Generates a random UUID at startup and prints it with a timestamp every 5 seconds.

## Run
    # To create your custom image for application
    docker build -t YOUR_DOCKERHUB_USER/log-output:1.1 .
    docker push YOUR_DOCKERHUB_USER/log-output:1.1

    # To run existing application
    kubectl apply -f manifests/deployment.yaml
    kubectl logs -f deployment/hashgenerator-deployment
    