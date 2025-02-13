# 8. Labels, Annotations, and Namespaces in Kubernetes

## Labels

Labels are used to select resources in clusters. They also can be used to group and select objects in clusters.
Labels can be assigned while creatin the objects in cluster, and they also can be added later.
The labels are assigned by key:value pair.

The yaml file [kubernetes-pod-with-labels.yaml](./kubernetes-pod-with-labels.yaml) includes the labels as

```
  labels:
    environment: dev
    app: http-server
```

These labels in yaml file will be assigned to the pod.

**kubectl get pods**

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods
NAME               READY   STATUS    RESTARTS      AGE
app-kubernetes-1   1/1     Running   1 (21h ago)   26h
app-kubernetes-2   1/1     Running   1 (21h ago)   22h
```

**kubectl create -f .\kubernetes-pod-with-labels.yaml**

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl create -f .\kubernetes-pod-with-labels.yaml
pod/app-kubernetes-with-labels created
```

**kubectl get pods**

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods
NAME                         READY   STATUS    RESTARTS      AGE
app-kubernetes-1             1/1     Running   1 (21h ago)   26h
app-kubernetes-2             1/1     Running   1 (21h ago)   22h
app-kubernetes-with-labels   1/1     Running   0             3s
```

**kubectl get pods --show-labels**

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods --show-labels
NAME                         READY   STATUS    RESTARTS      AGE   LABELS
app-kubernetes-1             1/1     Running   1 (21h ago)   26h   run=app-kubernetes-1
app-kubernetes-2             1/1     Running   1 (21h ago)   22h   <none>
app-kubernetes-with-labels   1/1     Running   0             22s   app=http-server,environment=dev
```

The pod with label run=app-kubernetes-1 have recieved such label, since it was added manually using cli. In that case the label run=app-kubernetes-1 has been assigned automatically.

This can be checked by deploying one more pod...

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl run app-kubernetes-manual --image=kmi8000/kubernetes_multi:0.1 --port=8000
pod/app-kubernetes-manual created

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods --show-labels
NAME                         READY   STATUS    RESTARTS      AGE   LABELS
app-kubernetes-1             1/1     Running   1 (22h ago)   27h   run=app-kubernetes-1
app-kubernetes-2             1/1     Running   1 (22h ago)   23h   <none>
app-kubernetes-manual        1/1     Running   0             3s    run=app-kubernetes-manual
app-kubernetes-with-labels   1/1     Running   0             47m   app=http-server,environment=dev

```

In case we need to select specific labels, the L swuth can be added to the get command.

To assign label to the running pod issue the command `kubectl label pod app-kubernetes-1 environment=dev`.

`kubectl get pods -L app,environment,run` the comma symbol **,** works like **AND** operator.

The output

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods -L app,environment,run
NAME                         READY   STATUS    RESTARTS      AGE   APP           ENVIRONMENT   RUN
app-kubernetes-1             1/1     Running   1 (22h ago)   27h                 dev           app-kubernetes-1
app-kubernetes-2             1/1     Running   1 (22h ago)   23h
app-kubernetes-manual        1/1     Running   0             10m                               app-kubernetes-manual
app-kubernetes-with-labels   1/1     Running   0             58m   http-server   dev
```

The labels can be selected by operators, such as `=` `==` `!=`. First two are synonyms and stands for EQUAL, accordingly the `!=` stands for NOT EQUAL.
additional operators are `in` and `notin` which are basically the same as EQUAL and NOT EQUAL.

The operators can be combined to filter results more precisely.

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods -l run
NAME                    READY   STATUS    RESTARTS      AGE
app-kubernetes-1        1/1     Running   1 (22h ago)   27h
app-kubernetes-manual   1/1     Running   0             20m

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods -l !run
NAME                         READY   STATUS    RESTARTS      AGE
app-kubernetes-2             1/1     Running   1 (22h ago)   23h
app-kubernetes-with-labels   1/1     Running   0             68m

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods -l 'environment in (dev)'
NAME                         READY   STATUS    RESTARTS      AGE
app-kubernetes-1             1/1     Running   1 (22h ago)   27h
app-kubernetes-with-labels   1/1     Running   0             70m

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods -l 'app notin (http-server)'
NAME                    READY   STATUS    RESTARTS      AGE
app-kubernetes-1        1/1     Running   1 (22h ago)   27h
app-kubernetes-2        1/1     Running   1 (22h ago)   23h
app-kubernetes-manual   1/1     Running   0             23m

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods -l app!=http-server
NAME                    READY   STATUS    RESTARTS      AGE
app-kubernetes-1        1/1     Running   1 (22h ago)   27h
app-kubernetes-2        1/1     Running   1 (22h ago)   23h
app-kubernetes-manual   1/1     Running   0             23m

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods -l run,environment=dev
NAME               READY   STATUS    RESTARTS      AGE
app-kubernetes-1   1/1     Running   1 (22h ago)   27h 
```

The labels can be also assigned to the Nodes.

Let's assume we have many nodes, and one of them have GPU. We can label that node with label gpu=true

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl label node minikube gpu=true
node/minikube labeled

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get nodes -l gpu=true
NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   2d1h   v1.32.0
```

If we issue command ` kubectl describe nodes minikube` we can see that the label gpu=true has been assigned to the minikube node.

The output

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl describe nodes minikube
Name:               minikube
Roles:              control-plane
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    gpu=true

output ommited...
```

Since we can label the nodes, we then can deploy a new pod and use the label as a selector on wich node the pod nust be deployed.

For that the new manifest kubernetes-pod-with-gpu.yaml file will be used [kubernetes-pod-with-gpu.yaml](./kubernetes-pod-with-gpu.yaml) which has instructions like...

```
apiVersion: v1
kind: Pod
metadata:
  name: app-kubernetes-with-gpu
  labels:
    app: http-server
spec:
  nodeSelector:
    gpu: "true"
  containers:
  - name: app-kubernetes-container
    image: kmi8000/kubernetes_multi:0.1
    ports:
    - containerPort: 8000
```

Deploying the kubernetes-pod-with-gpu.yaml

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl apply -f .\kubernetes-pod-with-gpu.yaml
pod/app-kubernetes-with-gpu created

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get pods
NAME                         READY   STATUS    RESTARTS      AGE
app-kubernetes-1             1/1     Running   1 (23h ago)   28h
app-kubernetes-2             1/1     Running   1 (23h ago)   24h
app-kubernetes-manual        1/1     Running   0             61m
app-kubernetes-with-gpu      1/1     Running   0             45s
app-kubernetes-with-labels   1/1     Running   0             108m

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl.exe describe pod app-kubernetes-with-gpu
Name:             app-kubernetes-with-gpu
Namespace:        default
Priority:         0
Service Account:  default
Node:             minikube/192.168.16.132
Start Time:       Thu, 13 Feb 2025 01:56:12 +0200
Labels:           app=http-server

output ommited...
```

## Annotations

Annotations are used to add metadata to the objects, there is not annotations selector, the pods cannot be selected by annotations.

They are used mostly to add descriptions to the pods, for example to add annotation to the app-kubernetes-2 we can issue `kubectl annotate pod app-kubernetes-2 company-name/creator-email="developer@example.com"`command.

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl.exe describe pod app-kubernetes-2
Name:             app-kubernetes-2
Namespace:        default
Priority:         0
Service Account:  default
Node:             minikube/192.168.16.132
Start Time:       Wed, 12 Feb 2025 01:33:35 +0200
Labels:           <none>
Annotations:      company-name/creator-email: developer@example.com 

output ommited
```

## Namespaces

Kubernetes supports several virtual clusters in one physical cluster. These virtual clusters are calling Namespaces.
The names of the resources can be the same in the separate Namespaces.

Let's create new namespaces, by [namespace.yaml](./namespace.yaml) file and manually `kubectl create namespace qa `.

code of namespace.yaml file.

```
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```

Apllying commands...

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get namespaces
NAME                   STATUS   AGE
default                Active   2d2h
kube-node-lease        Active   2d2h
kube-public            Active   2d2h
kube-system            Active   2d2h
kubernetes-dashboard   Active   2d1h

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl apply -f .\namespace.yaml
namespace/dev created

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get namespaces
NAME                   STATUS   AGE
default                Active   2d2h
dev                    Active   7s
kube-node-lease        Active   2d2h
kube-public            Active   2d2h
kube-system            Active   2d2h
kubernetes-dashboard   Active   2d2h

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl create namespace qa
namespace/qa created

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes> kubectl get namespaces
NAME                   STATUS   AGE
default                Active   2d2h
dev                    Active   33s
kube-node-lease        Active   2d2h
kube-public            Active   2d2h
kube-system            Active   2d2h
kubernetes-dashboard   Active   2d2h
qa                     Active   6s
```

Since the namespaces are already created, we can apply new manifest file [deb-qa-apps.yaml](./dev-qa-apps.yaml) to deploy several pods in newly created namespaces.

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl.exe get pods --all-namespaces
NAMESPACE              NAME                                         READY   STATUS    RESTARTS        AGE
default                app-kubernetes-1                             1/1     Running   1 (24h ago)     29h
default                app-kubernetes-2                             1/1     Running   1 (24h ago)     25h
default                app-kubernetes-manual                        1/1     Running   0               103m
default                app-kubernetes-with-gpu                      1/1     Running   0               42m
default                app-kubernetes-with-labels                   1/1     Running   0               150m
kube-system            coredns-668d6bf9bc-js4kv                     1/1     Running   2 (24h ago)     2d2h
kube-system            coredns-668d6bf9bc-kkv6p                     1/1     Running   2 (24h ago)     2d2h
kube-system            etcd-minikube                                1/1     Running   2 (24h ago)     2d2h
kube-system            kube-apiserver-minikube                      1/1     Running   2 (24h ago)     2d2h
kube-system            kube-controller-manager-minikube             1/1     Running   2 (24h ago)     2d2h
kube-system            kube-proxy-s252l                             1/1     Running   2 (24h ago)     2d2h
kube-system            kube-scheduler-minikube                      1/1     Running   2 (24h ago)     2d2h
kube-system            metrics-server-7fbb699795-gwm9b              1/1     Running   2 (24h ago)     2d2h
kube-system            storage-provisioner                          1/1     Running   5 (5h49m ago)   2d2h
kubernetes-dashboard   dashboard-metrics-scraper-5d59dccf9b-74rjf   1/1     Running   2 (24h ago)     2d2h
kubernetes-dashboard   kubernetes-dashboard-7779f9b69b-ddfdj        1/1     Running   2 (24h ago)     2d2h

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl apply -f .\dev-qa-apps.yaml
pod/app-kubernetes-qa-1 created
pod/app-kubernetes-qa-2 created
pod/app-kubernetes-dev-1 created
pod/app-kubernetes-dev-2 created

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl.exe get pods --all-namespaces
NAMESPACE              NAME                                         READY   STATUS    RESTARTS        AGE
default                app-kubernetes-1                             1/1     Running   1 (24h ago)     29h
default                app-kubernetes-2                             1/1     Running   1 (24h ago)     25h
default                app-kubernetes-manual                        1/1     Running   0               103m
default                app-kubernetes-with-gpu                      1/1     Running   0               43m
default                app-kubernetes-with-labels                   1/1     Running   0               151m
dev                    app-kubernetes-dev-1                         1/1     Running   0               4s
dev                    app-kubernetes-dev-2                         1/1     Running   0               4s
kube-system            coredns-668d6bf9bc-js4kv                     1/1     Running   2 (24h ago)     2d2h
kube-system            coredns-668d6bf9bc-kkv6p                     1/1     Running   2 (24h ago)     2d2h
kube-system            etcd-minikube                                1/1     Running   2 (24h ago)     2d2h
kube-system            kube-apiserver-minikube                      1/1     Running   2 (24h ago)     2d2h
kube-system            kube-controller-manager-minikube             1/1     Running   2 (24h ago)     2d2h
kube-system            kube-proxy-s252l                             1/1     Running   2 (24h ago)     2d2h
kube-system            kube-scheduler-minikube                      1/1     Running   2 (24h ago)     2d2h
kube-system            metrics-server-7fbb699795-gwm9b              1/1     Running   2 (24h ago)     2d2h
kube-system            storage-provisioner                          1/1     Running   5 (5h49m ago)   2d2h
kubernetes-dashboard   dashboard-metrics-scraper-5d59dccf9b-74rjf   1/1     Running   2 (24h ago)     2d2h
kubernetes-dashboard   kubernetes-dashboard-7779f9b69b-ddfdj        1/1     Running   2 (24h ago)     2d2h
qa                     app-kubernetes-qa-1                          1/1     Running   0               4s
qa                     app-kubernetes-qa-2                          1/1     Running   0               4s
```

We can delete pods by using several methods, by using manifest files, manually or using labels.

```
H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl delete pods app-kubernetes-2
pod "app-kubernetes-2" deleted

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl get pods --all-namespaces
NAMESPACE              NAME                                         READY   STATUS    RESTARTS        AGE
default                app-kubernetes-1                             1/1     Running   1 (24h ago)     29h
default                app-kubernetes-manual                        1/1     Running   0               111m
default                app-kubernetes-with-gpu                      1/1     Running   0               50m
default                app-kubernetes-with-labels                   1/1     Running   0               158m
dev                    app-kubernetes-dev-1                         1/1     Running   0               7m30s
dev                    app-kubernetes-dev-2                         1/1     Running   0               7m30s
kube-system            coredns-668d6bf9bc-js4kv                     1/1     Running   2 (24h ago)     2d3h
kube-system            coredns-668d6bf9bc-kkv6p                     1/1     Running   2 (24h ago)     2d3h
kube-system            etcd-minikube                                1/1     Running   2 (24h ago)     2d3h
kube-system            kube-apiserver-minikube                      1/1     Running   2 (24h ago)     2d3h
kube-system            kube-controller-manager-minikube             1/1     Running   2 (24h ago)     2d3h
kube-system            kube-proxy-s252l                             1/1     Running   2 (24h ago)     2d3h
kube-system            kube-scheduler-minikube                      1/1     Running   2 (24h ago)     2d3h
kube-system            metrics-server-7fbb699795-gwm9b              1/1     Running   2 (24h ago)     2d2h
kube-system            storage-provisioner                          1/1     Running   5 (5h57m ago)   2d3h
kubernetes-dashboard   dashboard-metrics-scraper-5d59dccf9b-74rjf   1/1     Running   2 (24h ago)     2d2h
kubernetes-dashboard   kubernetes-dashboard-7779f9b69b-ddfdj        1/1     Running   2 (24h ago)     2d2h
qa                     app-kubernetes-qa-1                          1/1     Running   0               7m30s
qa                     app-kubernetes-qa-2                          1/1     Running   0               7m30s

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl delete -f .\kubernetes-pod-with-labels.yaml
pod "app-kubernetes-with-labels" deleted

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl get pods -L app,environment,run
NAME                      READY   STATUS    RESTARTS      AGE    APP           ENVIRONMENT   RUN
app-kubernetes-1          1/1     Running   1 (24h ago)   29h                  dev           app-kubernetes-1
app-kubernetes-manual     1/1     Running   0             113m                               app-kubernetes-manual
app-kubernetes-with-gpu   1/1     Running   0             52m    http-server

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl delete pods -l run=app-kubernetes-manual
pod "app-kubernetes-manual" deleted

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl get pods --all-namespaces
NAMESPACE              NAME                                         READY   STATUS    RESTARTS       AGE
default                app-kubernetes-1                             1/1     Running   1 (24h ago)    29h
default                app-kubernetes-with-gpu                      1/1     Running   0              54m
dev                    app-kubernetes-dev-1                         1/1     Running   0              11m
dev                    app-kubernetes-dev-2                         1/1     Running   0              11m
kube-system            coredns-668d6bf9bc-js4kv                     1/1     Running   2 (24h ago)    2d3h
kube-system            coredns-668d6bf9bc-kkv6p                     1/1     Running   2 (24h ago)    2d3h
kube-system            etcd-minikube                                1/1     Running   2 (24h ago)    2d3h
kube-system            kube-apiserver-minikube                      1/1     Running   2 (24h ago)    2d3h
kube-system            kube-controller-manager-minikube             1/1     Running   2 (24h ago)    2d3h
kube-system            kube-proxy-s252l                             1/1     Running   2 (24h ago)    2d3h
kube-system            kube-scheduler-minikube                      1/1     Running   2 (24h ago)    2d3h
kube-system            metrics-server-7fbb699795-gwm9b              1/1     Running   2 (24h ago)    2d2h
kube-system            storage-provisioner                          1/1     Running   5 (6h1m ago)   2d3h
kubernetes-dashboard   dashboard-metrics-scraper-5d59dccf9b-74rjf   1/1     Running   2 (24h ago)    2d2h
kubernetes-dashboard   kubernetes-dashboard-7779f9b69b-ddfdj        1/1     Running   2 (24h ago)    2d2h
qa                     app-kubernetes-qa-1                          1/1     Running   0              11m
qa                     app-kubernetes-qa-2                          1/1     Running   0              11m

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl delete namespaces qa
namespace "qa" deleted
                                                                                                                                                             H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl delete -f .\namespace.yaml
namespace "dev" deleted

H:\GitHub\k8s\8. Labels, Annotations, and Namespaces in Kubernetes > kubectl get pods --all-namespaces
NAMESPACE              NAME                                         READY   STATUS    RESTARTS       AGE
default                app-kubernetes-1                             1/1     Running   1 (24h ago)    29h
default                app-kubernetes-with-gpu                      1/1     Running   0              56m
kube-system            coredns-668d6bf9bc-js4kv                     1/1     Running   2 (24h ago)    2d3h
kube-system            coredns-668d6bf9bc-kkv6p                     1/1     Running   2 (24h ago)    2d3h
kube-system            etcd-minikube                                1/1     Running   2 (24h ago)    2d3h
kube-system            kube-apiserver-minikube                      1/1     Running   2 (24h ago)    2d3h
kube-system            kube-controller-manager-minikube             1/1     Running   2 (24h ago)    2d3h
kube-system            kube-proxy-s252l                             1/1     Running   2 (24h ago)    2d3h
kube-system            kube-scheduler-minikube                      1/1     Running   2 (24h ago)    2d3h
kube-system            metrics-server-7fbb699795-gwm9b              1/1     Running   2 (24h ago)    2d2h
kube-system            storage-provisioner                          1/1     Running   5 (6h3m ago)   2d3h
kubernetes-dashboard   dashboard-metrics-scraper-5d59dccf9b-74rjf   1/1     Running   2 (24h ago)    2d2h
kubernetes-dashboard   kubernetes-dashboard-7779f9b69b-ddfdj        1/1     Running   2 (24h ago)    2d2h  
```