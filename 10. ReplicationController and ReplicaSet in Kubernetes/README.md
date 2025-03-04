# 9. ReplicationController and ReplicaSet in Kubernetes

ReplicationController keep amount of pods according to the min and max settings.

The following code of rc-kubernetesyamlyaml file creates the ReplicationController with 3 replicas of pods with label as http-server. The template: part describes what kind of containers must be deployed.

```
apiVersion: v1
kind: ReplicationController
metadata:
  name: kubernetes-rc
spec:
  replicas: 3
  selector:
    app: http-server
  template:
    metadata:
      name: kubernetes-app
      labels:
        app: http-server
    spec:
      containers:
      - name: http-server-image
        image: kmi8000/kubernetes_multi
        ports:
        - containerPort: 8000
```