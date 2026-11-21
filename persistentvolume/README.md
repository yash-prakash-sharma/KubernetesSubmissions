# Persistent volume

Cluster-level storage shared by the ping-pong and log-output applications.
It is kept separate from the apps, as a cluster administrator would manage it.

## Setup
The volume is a local volume on the node `k3d-k3s-default-agent-0`, so the directory must exist first:

    docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube

If the cluster is recreated, run this again. Check node names with `kubectl get nodes`.

## Deploy
Apply this before the applications:

    kubectl apply -f persistentvolume/

Contains a PersistentVolume (1Gi, storage class `shared-storage`) and a
PersistentVolumeClaim (`shared-pvc`) that both applications mount at `/data`.