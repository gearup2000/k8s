# Deployment in Kubernetes. Application Update Strategies

Kubernetes deployments manage the lifecycle of applications, including scaling, updating, and rolling back pods. Key strategies include Recreate, Rolling Update, Blue-Green, and Canary, each offering different methods for updating applications with minimal downtime.

The deployment is the highe level of resources in Kubernetes. In includeds the services, like: Replication Controllers, ReplicaSet and others. Deployments are responsible for creating, scaling, and updating the application's pods.

Deployment strategies provide a way to manage the deployment of applications in Kubernetes. They define the order in which the containers are deployed, the actions taken when a new version of the application is deployed, and the strategy for scaling the application. The primary deployment strategies in Kubernetes include:
1. **Recreate**: Restarts all the replicas of the deployment.
2. **Rolling Update**: Updates the replicas one by one, ensuring that no pod is terminated during the update.
3. **Blue-Green**: Creates a new deployment with a new version of the application, and gradually deploys it to the existing pods, while the old pods are terminated.
4. **Canary Deployment**: Creates a new deployment with a new version of the application, and gradually deploys it to a subset of the pods, while the old pods are terminated.

Before start the Deployment part, let's clean up the cluster by `kubectl get all --all-namespaces` and `kubectl delete rs kubernetes-rs-2` commands.

Next let's create a deployment using the following command: `kubectl create deployment kubernetes-ctl-app --image=kmi8000/k8sphp_multi --replicas=3`

This command creates a deployment named `kubernetes-ctl-app` with 3 replicas of the image `kmi8000/k8sphp_multi`. That can be checked with `kubectl get deployments.apps -o yaml` command.

Output:

```
PS H:\GitHub\k8s> kubectl get deployments.apps -o yaml
apiVersion: v1
items:
- apiVersion: apps/v1
  kind: Deployment
  metadata:
    annotations:
      deployment.kubernetes.io/revision: "1"
    creationTimestamp: "2025-03-07T08:42:00Z"
    generation: 1
    labels:
      app: kubernetes-ctl-app
    name: kubernetes-ctl-app
    namespace: default
    resourceVersion: "29137"
    uid: c96f02f5-8ff5-471d-ac2e-dd1c14430ce1
  spec:
    progressDeadlineSeconds: 600
    replicas: 3
    revisionHistoryLimit: 10
    selector:
      matchLabels:
        app: kubernetes-ctl-app
    strategy:
      rollingUpdate:
        maxSurge: 25%
        maxUnavailable: 25%
      type: RollingUpdate
    template:
      metadata:
        creationTimestamp: null
        labels:
          app: kubernetes-ctl-app
      spec:
        containers:
        - image: kmi8000/k8sphp_multi
          imagePullPolicy: Always
          name: k8sphp-multi-slmwl
          resources: {}
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
        dnsPolicy: ClusterFirst
        restartPolicy: Always
        schedulerName: default-scheduler
        securityContext: {}
        terminationGracePeriodSeconds: 30
  status:
    availableReplicas: 3
    conditions:
    - lastTransitionTime: "2025-03-07T08:42:06Z"
      lastUpdateTime: "2025-03-07T08:42:06Z"
      message: Deployment has minimum availability.
      reason: MinimumReplicasAvailable
      status: "True"
      type: Available
    - lastTransitionTime: "2025-03-07T08:42:00Z"
      lastUpdateTime: "2025-03-07T08:42:06Z"
      message: ReplicaSet "kubernetes-ctl-app-7657bdd5c7" has successfully progressed.
      reason: NewReplicaSetAvailable
      status: "True"
      type: Progressing
    observedGeneration: 1
    readyReplicas: 3
    replicas: 3
    updatedReplicas: 3
kind: List
metadata:
  resourceVersion: ""
PS H:\GitHub\k8s>
```
So we can see that the deployment has ReplicaSet named `kubernetes-ctl-app-7657bdd5c7` of 3 replicas of the application even we did not used any specific command to create it, the . The containers named `k8sphp-multi-slmwl` are running and ready. The name was gained from docker images, since we used command to point to the image `kmi8000/k8sphp_multi`. Therefore, Kubernetes pulled the image from the specified registry and started the container with the same name as an image.

Let's change the docker image and update the deployment: `kubectl set image deployment/kubernetes-ctl-app k8sphp-multi=kmi8000/kubernetes_multi:0.1 --record`

Output:
```
PS H:\GitHub\k8s> kubectl set image deployment/kubernetes-ctl-app k8sphp-multi-slmwl=kmi8000/kubernetes_multi:0.1 --record
Flag --record has been deprecated, --record will be removed in the future
deployment.apps/kubernetes-ctl-app image updated
```

After changing the image, the deployment created a new ReplicaSet named `kubernetes-ctl-app-67996869d5` with 3 replicas of the new Docker image. But the old ReplicaSet still exsting, but with no pods. In output example below can be seen that new pods are running and ready and the part of their name prefixes are copied from the new ReplicaSet and proves that pods are part of the new ReplicaSet.:

```
PS H:\GitHub\k8s> kubectl get pods
NAME                                  READY   STATUS    RESTARTS   AGE
kubernetes-ctl-app-786ffb64cb-5nvz7   1/1     Running   0          11m
kubernetes-ctl-app-786ffb64cb-r4bg2   1/1     Running   0          11m
kubernetes-ctl-app-786ffb64cb-sfg59   1/1     Running   0          13m
PS H:\GitHub\k8s> kubectl get rs  
NAME                            DESIRED   CURRENT   READY   AGE
kubernetes-ctl-app-7657bdd5c7   0         0         0       3h15m
kubernetes-ctl-app-786ffb64cb   3         3         3       13m
```
The name of the pods are constructed from the name of deployment, the index of ReplicaSet and the index of pod within the ReplicaSet.

Let's clean again `kubectl delete -n default deployment kubernetes-ctl-app`.

This example was to demonstrate that deployment can be done using just a single row of commands in CLI.

