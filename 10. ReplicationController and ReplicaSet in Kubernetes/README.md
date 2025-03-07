# ReplicationController and ReplicaSet in Kubernetes

## Overview

A ReplicationController is one of the original replication types in Kubernetes that ensures a specified number of pod replicas are running at all times.

## File Structure Explanation

```yaml
# Define the API version - v1 is used for core Kubernetes resources like ReplicationController
apiVersion: v1

# Specify the resource type as ReplicationController
kind: ReplicationController

# Metadata section contains information about the resource
metadata:
name: kubernetes-rc  # Name of the ReplicationController

# Specification section defines desired state
spec:
# Number of identical pods to maintain
replicas: 3

# Selector defines how the RC identifies which pods to manage
# Simple equality-based selector (older style)
selector:
    app: kubernetes

# Template defines the pod specification to use when creating new pods
template:
    metadata:
    name: kubernetes-app  # Name for the pods
    labels:
        app: kubernetes  # Label that matches the selector above
    spec:
    containers:
    # Container configuration
    - name: kubernetes-app-image  # Name of the container
        image: kmi8000/k8sphp_multi  # Docker image to use
        ports:
        - containerPort: 8000  # Port the container exposes
```

## Key Points

1. **Purpose**: Maintains exactly 3 replicas of the specified pod at all times.
2. **Self-Healing**: If a pod fails, is deleted, or terminated, the ReplicationController automatically creates a replacement.
3. **Simple Scaling**: Change the `replicas` value to scale up or down.
4. **Pod Template**: Contains the exact specification for pods that will be created.
5. **Selector**: Uses label-based selection to identify which pods it manages.

## Historical Context

ReplicationController is considered a legacy resource in modern Kubernetes. For new applications, consider using:

- **ReplicaSet**: Improved version with set-based selectors
- **Deployment**: Higher-level resource that manages ReplicaSets and provides declarative updates

## Use Cases

- Simple stateless applications needing high availability
- Ensuring continuous operation of services
- Basic horizontal scaling of pods

## Limitations

- Only supports equality-based selectors (not set-based)
- No built-in support for rolling updates (unlike Deployments)
- Limited versioning capabilities

This ReplicationController example demonstrates the foundational concept of pod replication in Kubernetes, though newer resources provide more sophisticated functionality.

## Cheking the amount of replicas by Lens

Open Lens, select **minikube** cluster, select Workloads, and click Replication Controllers, the name should be `kubernetes-rc`. You can see the current number of replicas.

Using the command `kubectl get pods -l app=kubernetes` will show all pods with the label `app=kubernetes`. We can delete one of the pods to see the new replica being created. To do so run `kubectl delete pod <pod-name>`. command, and see that in real time apply `kubectl get pods -l app=kubernetes --watch` in separate terminal to see the changes.

Example:

First terminal output:

```
PS H:\GitHub\k8s> kubectl get pods -l app=kubernetes
NAME                  READY   STATUS    RESTARTS   AGE
kubernetes-rc-5pq4d   1/1     Running   0          141m
kubernetes-rc-g6btd   1/1     Running   0          31m
kubernetes-rc-vqp49   1/1     Running   0          91s
PS H:\GitHub\k8s> kubectl delete pod kubernetes-rc-5pq4d                 
pod "kubernetes-rc-5pq4d" deleted
PS H:\GitHub\k8s> 
```

Second terminal output:

```
PS H:\GitHub\k8s> kubectl get pods -l app=kubernetes --watch
NAME                  READY   STATUS    RESTARTS   AGE
kubernetes-rc-5pq4d   1/1     Running   0          141m
kubernetes-rc-g6btd   1/1     Running   0          31m
kubernetes-rc-vqp49   1/1     Running   0          2m9s
kubernetes-rc-5pq4d   1/1     Terminating   0          141m
kubernetes-rc-mjrhf   0/1     Pending       0          0s
kubernetes-rc-mjrhf   0/1     Pending       0          0s
kubernetes-rc-mjrhf   0/1     ContainerCreating   0          0s
kubernetes-rc-5pq4d   0/1     Completed           0          141m
kubernetes-rc-5pq4d   0/1     Completed           0          141m
kubernetes-rc-5pq4d   0/1     Completed           0          141m
kubernetes-rc-mjrhf   1/1     Running             0          3s
```

As can be seen, the new replica `kubernetes-rc-mjrhf` was created, and the old replica `kubernetes-rc-5pq4d` was terminated.

Let's create one extra pod with the same labels to see the behavior of Replication Controller.
To do so let's create a new manifest file `kubernetes-rc-extra-test.yaml` with the following content:

```
apiVersion: v1
kind: Pod
metadata:
  name: kubernetes-app-manual
  labels:
    app: kubernetes
spec:
  containers:
  - name: kubernetes-app-image
    image: kmi8000/k8sphp_multi
    ports:
    - containerPort: 8000
```

As can be seen, this pod has the same labels as the Replication Controller. Now let's apply this manifest:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl apply -f .\kubernetes-rc-extra-test.yaml
pod/kubernetes-app-manual created
```

So the manifest was applied successfully. Now let's check the status of the pods:

```
PS H:\GitHub\k8s> kubectl get pods -l app=kubernetes  
NAME                  READY   STATUS    RESTARTS   AGE
kubernetes-rc-g6btd   1/1     Running   0          135m
kubernetes-rc-mjrhf   1/1     Running   0          104m
kubernetes-rc-vqp49   1/1     Running   0          106m
```

As can be seen, there are still 3 pods with the label `app=kubernetes`. The kubernetes API has accepted the command but did not create the extra pod because the Replication Controller already had 3 replicas.

Let's create a new manifest file `kubernetes-rc-extra-test-with-different-label.yaml` with the following content:

```
apiVersion: v1
kind: Pod
metadata:
  name: kubernetes-app-manual
  labels:
    app: kubernetes-new-label
spec:
  containers:
  - name: kubernetes-app-image
    image: kmi8000/k8sphp_multi
    ports:
    - containerPort: 8000
```

And apply this manifest:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl apply -f .\kubernetes-rc-extra-test-with-different-label.yaml
pod/kubernetes-app-manual created
```

Let's check the status of the pods again:

```
PS H:\GitHub\k8s> kubectl get pods -A
NAMESPACE     NAME                               READY   STATUS    RESTARTS        AGE
default       kubernetes-app-manual              1/1     Running   0               23s
default       kubernetes-rc-g6btd                1/1     Running   0               140m
default       kubernetes-rc-mjrhf                1/1     Running   0               109m
default       kubernetes-rc-vqp49                1/1     Running   0               111m
kube-system   coredns-668d6bf9bc-bknvv           1/1     Running   0               4h24m
kube-system   etcd-minikube                      1/1     Running   0               4h24m
kube-system   kube-apiserver-minikube            1/1     Running   0               4h24m
kube-system   kube-controller-manager-minikube   1/1     Running   0               4h24m
kube-system   kube-proxy-vmq57                   1/1     Running   0               4h24m
kube-system   kube-scheduler-minikube            1/1     Running   0               4h24m
kube-system   storage-provisioner                1/1     Running   1 (4h23m ago)   4h24m
```

As can be seen, there are still 3 pods with the label `app=kubernetes` and 1 pod with the label `kubernetes-app-manual`. The kubernetes API has accepted the command but did not add it to the Replication Controller, since it has different labels. Let's change the label of this pod manually, so it can correlate with the labels od pods of Replication Controller:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl label pod kubernetes-app-manual app=kubernetes --overwrite
pod/kubernetes-app-manual labeled
```

The pod should now be labeled with the same label as the Replication Controller. Let's check the status of the pods again:

```
PS H:\GitHub\k8s> kubectl get pods --watch
NAME                    READY   STATUS    RESTARTS   AGE
kubernetes-app-manual   1/1     Running   0          31s
kubernetes-rc-g6btd     1/1     Running   0          156m
kubernetes-rc-mjrhf     1/1     Running   0          124m
kubernetes-rc-vqp49     1/1     Running   0          126m
kubernetes-app-manual   1/1     Running   0          3m53s
kubernetes-app-manual   1/1     Running   0          3m53s
kubernetes-app-manual   1/1     Terminating   0          3m53s
kubernetes-app-manual   0/1     Completed     0          3m54s
kubernetes-app-manual   0/1     Completed     0          3m55s
kubernetes-app-manual   0/1     Completed     0          3m55s
```

As can be seen, the pod with the label `app=kubernetes` has been terminated again since the amount of replicas has reached the desired state. So we tried to terminate one pod and also add one pod with the same label to the Replication Controller. Basically, Replication Controller is a simple and efficient way to replicate Pods in Kubernetes. It automatically handles the up-scaling or down-scaling of Pods based on the desired state.

We also can add labels to the existing pods using `kubectl label` command. For example by applying the following command: `kubectl label pod kubernetes-rc-vqp49 env=dev` we can add a label `env=dev` to the pod `kubernetes-rc-vqp49`.

Cheking the labels of the pods will show:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get pods --show-labels      
NAME                  READY   STATUS    RESTARTS   AGE    LABELS
kubernetes-rc-g6btd   1/1     Running   0          170m   app=kubernetes
kubernetes-rc-mjrhf   1/1     Running   0          139m   app=kubernetes
kubernetes-rc-vqp49   1/1     Running   0          141m   app=kubernetes,env=dev
```

As can be seen, the pod `kubernetes-rc-vqp49` has the label `env=dev`. But has not been terminated because it is also has the same label as the label of Replication Controller. So we can add extra labels to the pods without any problem.

In case we remove the label `app=kubernetes` from the pod `kubernetes-rc-vqp49`, it will be treated as a pod that does not belong to the Replication Controller, therefore Replication Controller will not manage it at all. But also, this will cause the Replication Controller to recreate the new pod `kubernetes-rc-<pod name>` with the original label `app=kubernetes`.

Let's do that to see the behavior of Replication Controller:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl label pod kubernetes-rc-mjrhf app=http-server --overwrite
pod/kubernetes-rc-mjrhf labeled

PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get pods --show-labels
NAME                  READY   STATUS    RESTARTS   AGE     LABELS
kubernetes-rc-g6btd   1/1     Running   0          3h19m   app=kubernetes
kubernetes-rc-mjrhf   1/1     Running   0          167m    app=http-server
kubernetes-rc-vqp49   1/1     Running   0          169m    app=kubernetes,env=dev
kubernetes-rc-xzqq8   1/1     Running   0          18s     app=kubernetes
```

As can be seen, the pod `kubernetes-rc-mjrhf` has been labeled with the label `app=http-server` and has been deregistered from Replication Controller since it has different label. The Replication Controller will recreate the new pod `kubernetes-rc-xzqq8` with the original label `app=kubernetes`. This can be very useful for trouble-shooting of unhealthy pod, check the logs, check the errors etc..

In case we need to rename containers of existing pods, we can change the settings in the manifest file and apply it again. However, the changes will not affect the existing pods. To apply the changes, we need recreate them with the new settings and delete the existing pods.

For example, let's change the name of the container, to do so let's make a copy of existing manifest file and change the name of the container:

```
apiVersion: v1
kind: ReplicationController
metadata:
  name: kubernetes-rc
spec:
  replicas: 3
  selector:
    app: kubernetes
  template:
    metadata:
      name: kubernetes-app
      labels:
        app: kubernetes
    spec:
      containers:
      - name: kubernetes-app-version-2-image
        image: kmi8000/k8sphp_multi
        ports:
        - containerPort: 8000
```

let's apply this manifest and check the status of the pods:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl apply -f .\rc-kubernetes-copy-with-different-container-name.yaml
replicationcontroller/kubernetes-rc configured
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get pods --show-labels
NAME                  READY   STATUS    RESTARTS   AGE     LABELS
kubernetes-rc-g6btd   1/1     Running   0          3h58m   app=kubernetes
kubernetes-rc-mjrhf   1/1     Running   0          3h26m   app=http-server
kubernetes-rc-vqp49   1/1     Running   0          3h29m   app=kubernetes,env=dev
kubernetes-rc-xzqq8   1/1     Running   0          39m     app=kubernetes

PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get pods -o jsonpath='{.items[*].spec.containers[*].name}'
kubernetes-app-image kubernetes-app-image kubernetes-app-image kubernetes-app-image
```

As can be seen, nothing has changed, we still have 4 pods, 3 of which are belongs to the existing Replication Controller and all 4 pods has the old name of container. Let's delete pod with name **kubernetes-rc-xzqq8** and check what will happen:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl delete pod kubernetes-rc-xzqq8
pod "kubernetes-rc-xzqq8" deleted

PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get pods --show-labels
NAME                  READY   STATUS    RESTARTS   AGE     LABELS
kubernetes-rc-g6btd   1/1     Running   0          4h5m    app=kubernetes
kubernetes-rc-mcbth   1/1     Running   0          11s     app=kubernetes
kubernetes-rc-mjrhf   1/1     Running   0          3h34m   app=http-server
kubernetes-rc-vqp49   1/1     Running   0          3h36m   app=kubernetes,env=dev

PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get pods -o jsonpath='{.items[*].spec.containers[*].name}'
kubernetes-app-image kubernetes-app-version-2-image kubernetes-app-image kubernetes-app-image
```

As can be seen, the Replication Controller created a new pod named `kubernetes-rc-mcbth` with the new name of container `kubernetes-app-version-2-image`. The old pods still use the old name of container `kubernetes-app-image`. This shows that the Replication Controller is not directly impacted by renaming containers of existing pods. Instead, it manages the number of pods based on the desired state. This means that we can easily change the name of containers without affecting the running pods. And change will be reflected only in the new pods created by the Replication Controller.

Let's remove all Replication Controllers and pods:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl delete pods -l app=http-server
pod "kubernetes-rc-mjrhf" deleted
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get replicationcontrollers  
NAME            DESIRED   CURRENT   READY   AGE
kubernetes-rc   3         3         3       6h3m
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl delete replicationcontrollers kubernetes-rc
replicationcontroller "kubernetes-rc" deleted
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get pods            
No resources found in default namespace.
```

## ReplicaSet

The ReplicaSet is a more advanced and flexible way to manage Pods in Kubernetes. It is a subset of Replication Controller and provides additional features. ReplicaSet is the recommended way to manage Pods in Kubernetes.

Let's create a new file named `rs-kubernetes.yaml` with the following content:

```
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: kubernetes-rs-1
  labels:
    app: kubernetes-rs
spec:
    replicas: 3
    selector:
      matchLabels:
        env: dev
    template:
      metadata:
        labels:
          env: dev
      spec:
        containers:
        - name: kubernetes-app
          image: kmi8000/k8sphp_multi
```

and apply it `kubectl apply -f rs-kubernetes.yaml`:

```PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl apply -f .\rs-kubernetes.yaml
replicaset.apps/kubernetes-rs-1 created

PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get pods --show-labels     
NAME                    READY   STATUS    RESTARTS   AGE     LABELS
kubernetes-rs-1-v78m9   1/1     Running   0          6m43s   env=dev
kubernetes-rs-1-x2862   1/1     Running   0          6m43s   env=dev
kubernetes-rs-1-zgtlm   1/1     Running   0          6m43s   env=dev
```

The ReplicaSet has created 3 pods with the label `env=dev`.

The next ReplicaSet manifest file nammed as `rs-kubernetes-matchExpressions.yaml` will create ReplicaSets of 3 pods:

```
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: kubernetes-rs-2
spec:
  replicas: 3
  selector:
    matchExpressions:
      - key: app
        operator: In
        values:
          - kubernetes
          - http-server
      - key: env
        operator: Exists
  template:
    metadata:
      labels:
        app: kuber
        env: dev
    spec:
      containers:
      - name: kubernetes-app
        image: kmi8000/k8sphp_multi 
```

However in the selector part there is some changes, the matchExpressions are used to match pods based on a set of conditions and operators (In, NotIn, Exists, DoesNotExist), in this example in the part:

```
    matchExpressions:
      - key: app
        operator: In
        values:
          - kubernetes
          - http-server
      - key: env
        operator: Exists
```

we are saying that the pods should have labels (key) as `app` and the value of that label (key) should be equal to `kubernetes` OR `http-server`, and label `env` should exist, and the value of that key does not matter.

Let's apply this manifest and check the status of the pods:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl apply -f .\rs-kubernetes-matchExpressions.yaml
replicaset.apps/kubernetes-rs-2 created
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get pods --show-labels  

NAME                    READY   STATUS    RESTARTS   AGE   LABELS
kubernetes-rs-1-v78m9   1/1     Running   0          29m   env=dev
kubernetes-rs-1-x2862   1/1     Running   0          29m   env=dev
kubernetes-rs-1-zgtlm   1/1     Running   0          29m   env=dev
kubernetes-rs-2-ph56n   1/1     Running   0          62s   app=kubernetes,env=dev
kubernetes-rs-2-pxmdn   1/1     Running   0          62s   app=kubernetes,env=dev
kubernetes-rs-2-t4mlc   1/1     Running   0          62s   app=kubernetes,env=dev

PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get rs --show-labels  
NAME              DESIRED   CURRENT   READY   AGE     LABELS
kubernetes-rs-1   3         3         3       30m     app=kubernetes-rs
kubernetes-rs-2   3         3         3       2m18s   <none>
```

As can be seen, the new ReplicaSet `kubernetes-rs-2` has created 3 pods with labels `app=kubernetes` and `env=dev`. As well the first ReplicaSet `kubernetes-rs-1` still has 3 pods.

Let's remove the ReplicaSet kubernetes-rs-1, since it was created just to show the differences with `kubernetes-rs-2`. We will use `kubectl delete rs kubernetes-rs-1`:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl delete rs kubernetes-rs-1
replicaset.apps "kubernetes-rs-1" deleted

PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
kubernetes-rs-2   3         3         3       27m

PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get pods -A
NAMESPACE     NAME                               READY   STATUS    RESTARTS     AGE
default       kubernetes-rs-2-ph56n              1/1     Running   0            30m
default       kubernetes-rs-2-pxmdn              1/1     Running   0            30m
default       kubernetes-rs-2-t4mlc              1/1     Running   0            30m
```

Let's create two more manifest files named as `kubernetes-pods-manual-commented-env.yaml`
with the following content:

```
apiVersion: v1
kind: Pod
metadata:
  name: kubernetes-app-manual-1
  labels:
    app: kubernetes
    # env: prod
spec:
  containers:
  - name: kubernetes-app-1
    image: kmi8000/k8sphp_multi
    ports:
    - containerPort: 8000
---
apiVersion: v1
kind: Pod
metadata:
  name: kubernetes-app-manual-2
  labels:
    app: http-server
    # env: dev
spec:
  containers:
  - name: kubernetes-app-1
    image: kmi8000/k8sphp_multi
    ports:
    - containerPort: 8000
```

and `kubernetes-pods-manual-uncommented-app.yaml` with the following content:

```
apiVersion: v1
kind: Pod
metadata:
  name: kubernetes-app-manual-1
  labels:
    app: kubernetes
    # env: prod
spec:
  containers:
  - name: kubernetes-app-1
    image: kmi8000/k8sphp_multi
    ports:
    - containerPort: 8000
---
apiVersion: v1
kind: Pod
metadata:
  name: kubernetes-app-manual-2
  labels:
    app: http-server
    # env: dev
spec:
  containers:
  - name: kubernetes-app-1
    image: kmi8000/k8sphp_multi
    ports:
    - containerPort: 8000
```

The different manifest files are commented out with `# env: prod` and `# env: dev` respectively. Everything is the same, but the commented lines prevent the `env` label from being added to the Pods.In the commented manifest file `kubernetes-pods-manual-commented-env.yaml`, the `env` label is commented purposenly, so when we will apply this manifest, the ReplicaSet will see that the labels matches with its settings and the pods will NOT be created.

Let's apply `kubernetes-pods-manual-commented-env.yaml` manifests file:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl apply -f .\kubernetes-pods-manual-commented-env.yaml
pod/kubernetes-app-manual-1 created
pod/kubernetes-app-manual-2 created

 kubectl get pods --show-labels
NAME                      READY   STATUS    RESTARTS   AGE   LABELS
kubernetes-app-manual-1   1/1     Running   0          40s   app=kubernetes
kubernetes-app-manual-2   1/1     Running   0          40s   app=http-server
kubernetes-rs-2-ph56n     1/1     Running   0          33m   app=kubernetes,env=dev
kubernetes-rs-2-pxmdn     1/1     Running   0          33m   app=kubernetes,env=dev
kubernetes-rs-2-t4mlc     1/1     Running   0          33m   app=kubernetes,env=dev
```

After applying the commented manifest, the pods `kubernetes-app-manual-1` and `kubernetes-app-manual-2` are created with the label `app=kubernetes`. However, the pods are not created with the label `env=dev` as the commented lines prevent this label from being added to the Pods, therefore they are not managed by ReplicaSet `kubernetes-rs-2` since the part mentions above, particularly

```
      - key: env
        operator: Exists
```

saying that the env must exist, since there is no `env` labels (keys) in newly created 2 pods, the ReplicaSet just ignore them.

Now let's apply the uncommented manifest `kubernetes-pods-manual-uncommented-app.yaml` and check the status of the pods:

```
PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl apply -f .\kubernetes-pods-manual-uncommented-env.yaml
pod/kubernetes-app-manual-1 configured
pod/kubernetes-app-manual-2 configured

PS H:\GitHub\k8s\10. ReplicationController and ReplicaSet in Kubernetes> kubectl get pods --show-labels
NAME                      READY   STATUS        RESTARTS   AGE   LABELS
kubernetes-app-manual-1   0/1     Terminating   0          1s    app=kubernetes,env=prod
kubernetes-app-manual-2   0/1     Terminating   0          1s    app=http-server,env=dev
kubernetes-rs-2-ph56n     1/1     Running       0          42m   app=kubernetes,env=dev
kubernetes-rs-2-pxmdn     1/1     Running       0          42m   app=kubernetes,env=dev
kubernetes-rs-2-t4mlc     1/1     Running       0          42m   app=kubernetes,env=dev

```

As can be seen, the pods `kubernetes-app-manual-1` and `kubernetes-app-manual-2` are in a `Terminating` state. This is because the `env` labels. These labels matches with matchExpressions in the ReplicaSet's selector, so the pods are managed by the ReplicaSet, however since the desired amount of pods is 3, the ReplicaSet removes the two additional pods.
