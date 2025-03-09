# 12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints

For this chapter we need to create a cluster with at least 2 nodes. To do so aplly the command below:

`minikube start --nodes 2 -p multinode-demo`

Check the status of the cluster:

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl get nodes -o wide
NAME                 STATUS   ROLES           AGE   VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION                       CONTAINER-RUNTIME
multinode-demo       Ready    control-plane   24m   v1.32.0   192.168.49.2   <none>        Ubuntu 22.04.5 LTS   5.15.167.4-microsoft-standard-WSL2   docker://27.4.1
multinode-demo-m02   Ready    <none>          23m   v1.32.0   192.168.49.3   <none>        Ubuntu 22.04.5 LTS   5.15.167.4-microsoft-standard-WSL2   docker://27.4.1
```

Check the pods status: 
```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl get pods -o wide
NAME                          READY   STATUS    RESTARTS   AGE    IP           NODE                 NOMINATED NODE   READINESS GATES
kubernetes-6c85f7555c-mcxtw   1/1     Running   0          112s   10.244.1.2   multinode-demo-m02   <none>           <none>
kubernetes-6c85f7555c-wr676   1/1     Running   0          111s   10.244.1.3   multinode-demo-m02   <none>           <none>
kubernetes-6c85f7555c-zfwfz   1/1     Running   0          111s   10.244.0.3   multinode-demo       <none>           <none>
```
Since the pods are in running state, we can proceed to create a Service.

Let's apply a bew deployment manifest file we used in previous examples.

`kubectl apply -f kubernetes-deployment.yaml` and add a Service ClusterIP type by applying the following Service manifest file `kubectl apply -f clusterip-service.yaml`.

Let's check the status of the Service:

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl apply -f clusterip-service.yaml
service/kubernetes-service created
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl get svc
NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
kubernetes           ClusterIP   10.96.0.1       <none>        443/TCP   4h
kubernetes-service   ClusterIP   10.101.171.99   <none>        80/TCP    84s
```

The ClusterIP is 10.101.171.99. We can access the application using this IP. The Cluster IP service is accessible only within the cluster, and not from outside. If you want to access the application from outside the cluster, you need to expose the Service with a Service of type NodePort or LoadBalancer. 

Let's login to one of the nodes and check the ClusterIP service, to do so apply the following command `kubectl exec -it kubernetes-6c85f7555c-mcxtw -- bin/bash` and then apply the curl loop command that will sent http requests to the ClusterIP service `while true; do curl http://10.101.171.99/;sleep 2; echo; done`. Please note that you should replace `10.101.171.99` with the ClusterIP of the service.

The output should be similar to this:

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl exec -it kubernetes-6c85f7555c-mcxtw -- bin/bash 
root@kubernetes-6c85f7555c-mcxtw:/# while true; do curl http://10.101.171.99;sleep 2; echo; done
Hello world from hostname: kubernetes-6c85f7555c-zfwfz
Hello world from hostname: kubernetes-6c85f7555c-mcxtw
Hello world from hostname: kubernetes-6c85f7555c-wr676
Hello world from hostname: kubernetes-6c85f7555c-mcxtw
Hello world from hostname: kubernetes-6c85f7555c-zfwfz
Hello world from hostname: kubernetes-6c85f7555c-wr676
Hello world from hostname: kubernetes-6c85f7555c-zfwfz
Hello world from hostname: kubernetes-6c85f7555c-wr676
Hello world from hostname: kubernetes-6c85f7555c-wr676
Hello world from hostname: kubernetes-6c85f7555c-mcxtw
Hello world from hostname: kubernetes-6c85f7555c-zfwfz
Hello world from hostname: kubernetes-6c85f7555c-mcxtw
Output ommitted, use ^C to stop...
```
As can been seen, the service is working as expected, sending HTTP requests to the ClusterIP service and displaying the hostname of the pod it's sending the request to. The answers are showing the names of the pods running in the cluster. So the request is being load balanced across the pods. Remember this is not a load balancer, but a simple round-robin mechanism in this case. If you want a more robust load balancer, you should use a Kubernetes Ingress Controller or Cloud Load Balancer.

Let's now apply the `kubectl apply -f pod-service-port-names.yaml` file which includes the following code:

```
apiVersion: v1
kind: Pod
metadata:
  name: kubernetes-app-manual
  labels:
    app: web-server
spec:
  containers:
  - name: kubernetes-app-image
    image: kmi8000/kubernetes_multi:0.1
    ports:
    - name: http
      containerPort: 8000
    - name: https
      containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-app-manual-service
spec:
  selector:
    app: web-server
  ports:
  - name: http
    port: 80
    targetPort: http
  - name: https
    port: 443
    targetPort: https
```

Sure, here is a description of the `pod-service-port-names.yaml` file located in folder 12:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kubernetes-app-manual
  labels:
    app: web-server
spec:
  containers:
  - name: kubernetes-app-image
    image: kmi8000/kubernetes_multi:0.1
    ports:
    - name: http
      containerPort: 8000
    - name: https
      containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-app-manual-service
spec:
  selector:
    app: web-server
  ports:
  - name: http
    port: 80
    targetPort: http
  - name: https
    port: 443
    targetPort: https
```

This file creates a single Pod that listens on two ports (80 and 443) and assigns names to these ports (http and https). The Service `kubernetes-app-manual-service` targets the Pod with the label `app: web-server` and forwards traffic to the specified ports. This setup allows the Pod to handle traffic on both HTTP and HTTPS ports.

The naming of the ports can be handy in case you want to use a different port, for example we can change the port 8000 to 8001 in case we want it, that will not affect the Service, since it is using a names as a variable.

The output shows that we have duplicated ports for http and https which is 8000, but we will skip that for now.

```
Warning: spec.containers[0].ports[1]: duplicate port definition with spec.containers[0].ports[0]
pod/kubernetes-app-manual created
service/kubernetes-app-manual-service created
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints>
```

Check the pods to see that the new pod has been created.

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl get pods -o wide
NAME                          READY   STATUS    RESTARTS   AGE     IP           NODE                 NOMINATED NODE   READINESS GATES
kubernetes-6c85f7555c-mcxtw   1/1     Running   0          4h21m   10.244.1.2   multinode-demo-m02   <none>           <none>
kubernetes-6c85f7555c-wr676   1/1     Running   0          4h21m   10.244.1.3   multinode-demo-m02   <none>           <none>
kubernetes-6c85f7555c-zfwfz   1/1     Running   0          4h21m   10.244.0.3   multinode-demo       <none>           <none>
kubernetes-app-manual         1/1     Running   0          4m6s    10.244.1.4   multinode-demo-m02   <none>           <none>
```

We also got a new service, namly `kubernetes-app-manual-service`.

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl get services -o wide
NAME                            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE     SELECTOR
kubernetes                      ClusterIP   10.96.0.1        <none>        443/TCP          4h56m   <none>
kubernetes-app-manual-service   ClusterIP   10.109.188.145   <none>        80/TCP,443/TCP   5m15s   app=web-server
kubernetes-service              ClusterIP   10.101.171.99    <none>        80/TCP           57m     app=http-server
```

let's try to check the if we can reach the pod we just created. Login to any pods of kubernetes deployment and try to use `curl` command against of newly created ClusterIP service which is `10.109.188.145` in my case.

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl get services -o wide
NAME                            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE     SELECTOR
kubernetes                      ClusterIP   10.96.0.1        <none>        443/TCP          4h58m   <none>
kubernetes-app-manual-service   ClusterIP   10.109.188.145   <none>        80/TCP,443/TCP   7m11s   app=web-server
kubernetes-service              ClusterIP   10.101.171.99    <none>        80/TCP           59m     app=http-server
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl exec -it kubernetes-6c85f7555c-mcxtw -- bin/bash
root@kubernetes-6c85f7555c-mcxtw:/# curl http://10.109.188.145
Version 0.2
root@kubernetes-6c85f7555c-mcxtw:/#
```

let's remove the pod-service-port-names.yaml deployment configuration. 

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl delete -f .\pod-service-port-names.yaml
pod "kubernetes-app-manual" deleted
service "kubernetes-app-manual-service" deleted
```

let's now login to one of the pods, and check what environment variables does it have:

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl exec -it kubernetes-6c85f7555c-mcxtw -- bin/bash
root@kubernetes-6c85f7555c-mcxtw:/# env
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_SERVICE_PORT=443
HOSTNAME=kubernetes-6c85f7555c-mcxtw
PYTHON_VERSION=3.8.5
PWD=/
HOME=/root
LANG=C.UTF-8
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
TERM=xterm
SHLVL=1
KUBERNETES_PORT_443_TCP_PROTO=tcp
PYTHON_PIP_VERSION=20.2.3
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
PYTHON_GET_PIP_SHA256=6e0bb0a2c2533361d7f297ed547237caf1b7507f197835974c0dd7eba998c53c
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_PORT=443
PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/fa7dc83944936bf09a0e4cb5d5ec852c0d256599/get-pip.py
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/env
root@kubernetes-6c85f7555c-mcxtw:/#
```

The variables 
```
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_PORT=443
```
Has been gained by pod from ClusterIP service.

If we apply now command as `curl http://10.101.171.99` we will recieve the response from one of our pods. But we can also use DNS records of the ClusterIP service.
To find it we can see the resolv.conf file of the pod.

```
root@kubernetes-6c85f7555c-mcxtw:/# cat etc/resolv.conf 
nameserver 10.96.0.10
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

Let's use DNS record now:

```
Hello world from hostname: kubernetes-6c85f7555c-zfwfzroot@kubernetes-6c85f7555c-mcxtw:/# curl http://kubernetes-service.default.svc.cluster.local
Hello world from hostname: kubernetes-6c85f7555c-zfwfzroot@kubernetes-6c85f7555c-mcxtw:/# curl http://kubernetes-service.default.svc.cluster.local
Hello world from hostname: kubernetes-6c85f7555c-mcxtwroot@kubernetes-6c85f7555c-mcxtw:/# curl http://kubernetes-service.default.svc.cluster.local
Hello world from hostname: kubernetes-6c85f7555c-wr676root@kubernetes-6c85f7555c-mcxtw:/# curl http://kubernetes-service.default.svc.cluster.local
Hello world from hostname: kubernetes-6c85f7555c-mcxtwroot@kubernetes-6c85f7555c-mcxtw:/# curl http://kubernetes-service.default.svc.cluster.local
```
As can be found in the responses are coming from all 3 pods.

let's now install nslookup tool on that host, to do so aplly `apt update` and `apt-get install dnsutils`.

if we now aplly command `nslookup` towards the DNS name of the ClusterIP service, we will see that it returns the correct IP address of the ClisterIP kubernetes-service(10.101.171.99).

```
root@kubernetes-6c85f7555c-mcxtw:/# nslookup kubernetes-service.default.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   kubernetes-service.default.svc.cluster.local
Address: 10.101.171.99
```

We also can use just a name of the ClusterIP service, so the command will be `nslookup kubernetes-service`.

```
root@kubernetes-6c85f7555c-mcxtw:/# nslookup kubernetes-service
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   kubernetes-service.default.svc.cluster.local
Address: 10.101.171.99

root@kubernetes-6c85f7555c-mcxtw:/#
```
This is, because the service is in the same namespace as the the pod. In case we had a pod that is located in different namespace we would not be able to use the short name.

# Endpoints

1. Selector's role: The `selector` in a Service manifest is indeed not directly used for redirecting connections. Instead, it's used to identify which Pods should be associated with the Service.

2. Creating a list of endpoints: Based on the selector, Kubernetes creates a list of IP addresses and ports of the matching Pods. This list forms the "Endpoints" object associated with the Service.

3. Endpoints: These are essentially the backend Pods that the Service will route traffic to. The Endpoints object is automatically maintained by Kubernetes to reflect the current state of the Pods matching the Service's selector.

4. Service proxy: When a client connects to the Service's ClusterIP, the Kubernetes service proxy (which could be kube-proxy or a more advanced proxy depending on the cluster configuration) is responsible for choosing one of the endpoints and redirecting the incoming connection to the selected Pod.

5. Load balancing: The service proxy typically uses a simple round-robin algorithm to distribute incoming connections across the available endpoints, providing basic load balancing.

Let's bring back the pod we deleted earlier.

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl apply -f .\pod-service-port-names.yaml 
Warning: spec.containers[0].ports[1]: duplicate port definition with spec.containers[0].ports[0]
pod/kubernetes-app-manual created
service/kubernetes-app-manual-service created
```

And check the services we have.

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl get svc
NAME                            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes                      ClusterIP   10.96.0.1       <none>        443/TCP          8h
kubernetes-app-manual-service   ClusterIP   10.110.174.90   <none>        80/TCP,443/TCP   53s
kubernetes-service              ClusterIP   10.101.171.99   <none>        80/TCP           4h59m
```

As can be seen below, we have the kubernetes-app-manual-service and we aplly the command `kubectl get endpoints` we cab observe that we have endpoints for each servce we created.

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl get endpoints                      
NAME                            ENDPOINTS                                         AGE
kubernetes                      192.168.49.2:8443                                 9h
kubernetes-app-manual-service   10.244.1.5:8000,10.244.1.5:8000                   4m3s
kubernetes-service              10.244.0.3:8000,10.244.1.2:8000,10.244.1.3:8000   5h2m
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> 
```
In fact the `selector` of each services have registered the list of IP addresses and ports that belongs to it.

We can create a service without a `selector` and add endpoints manually.

In yaml files we used different version of Docker images, in `kubernetes` the Docker image is `kmi8000/kubernetes_multi:0.1` and in `kubernetes-app-manual-service` the Docker image is `kmi8000/kubernetes_multi:0.2`.

Let's register two different pods from services above as endpoints.
To do so let's create a new manifest file with name as `endpoints-service.yaml` that will have the code as:

```
apiVersion: v1
kind: Service
metadata:
  name: endpoints-service
spec:
  ports:
  - port: 80
---
apiVersion: v1
kind: Endpoints
metadata:
  name: endpoints-service
subsets:
  - addresses:
    - ip: 10.244.0.3
    - ip: 10.244.1.5
    ports:
    - port: 8000
```
and add the IP addresses of the endpoints from different services. So the `10.244.0.3` host have the Docker image version 0.1 and `10.244.1.5` have the version 0.2.
This can be checked by commands like:

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl get pods -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP           NODE                 NOMINATED NODE   READINESS GATES
kubernetes-6c85f7555c-mcxtw   1/1     Running   0          8h    10.244.1.2   multinode-demo-m02   <none>           <none>
kubernetes-6c85f7555c-wr676   1/1     Running   0          8h    10.244.1.3   multinode-demo-m02   <none>           <none>
kubernetes-6c85f7555c-zfwfz   1/1     Running   0          8h    10.244.0.3   multinode-demo       <none>           <none>
kubernetes-app-manual         1/1     Running   0          35m   10.244.1.5   multinode-demo-m02   <none>           <none>
```
and according to the output, we can describe particular pod, in our case they will be `kubernetes-6c85f7555c-zfwfz`, since it has the IP address as `10.244.0.3` and `kubernetes-app-manual` which has the IP address as `10.244.1.5`.

Let's check that they are based on different Docker images by applying `kubectl describe pod <pod name>` command.

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl describe pod kubernetes-6c85f7555c-zfwfz
Name:             kubernetes-6c85f7555c-zfwfz
Namespace:        default
Priority:         0
Service Account:  default
Node:             multinode-demo/192.168.49.2
Start Time:       Sat, 08 Mar 2025 18:28:32 +0200
Labels:           app=http-server
                  pod-template-hash=6c85f7555c
Annotations:      <none>
Status:           Running
IP:               10.244.0.3
IPs:
  IP:           10.244.0.3
Controlled By:  ReplicaSet/kubernetes-6c85f7555c
Containers:
  kubernetes-app:
    Container ID:   docker://3cd6ad8f7ac761763e0938b63f319ee53cc467fc569eb7c714031dcab9c1c039
    Image:          kmi8000/kubernetes_multi:0.1
    Image ID:       docker-pullable://kmi8000/kubernetes_multi@sha256:d88da6fb7b400bac387d85768304ef31b0cdac052852f70ec6acbf4a00b62bdf
    Port:           8000/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Sat, 08 Mar 2025 18:29:52 +0200
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-9l7g2 (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       True
  ContainersReady             True
  PodScheduled                True
Volumes:
  kube-api-access-9l7g2:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:                      <none>
```

and second pod:

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl describe pod kubernetes-app-manual      
Name:             kubernetes-app-manual
Namespace:        default
Priority:         0
Service Account:  default
Node:             multinode-demo-m02/192.168.49.3
Start Time:       Sun, 09 Mar 2025 02:52:32 +0200
Labels:           app=web-server
Annotations:      <none>
Status:           Running
IP:               10.244.1.5
IPs:
  IP:  10.244.1.5
Containers:
  kubernetes-app-image:
    Container ID:   docker://e0fc7600c0b720ce8f163636140e61b7720e06d1879b4ca2f570844112743281
    Image:          kmi8000/kubernetes_multi:0.2
    Image ID:       docker-pullable://kmi8000/kubernetes_multi@sha256:c9f4037790ae44fc993231946af4e466c2293a076717774990163ef5a78aade1
    Ports:          8000/TCP, 8000/TCP
    Host Ports:     0/TCP, 0/TCP
    State:          Running
      Started:      Sun, 09 Mar 2025 02:52:34 +0200
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-h7rtw (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       True
  ContainersReady             True
  PodScheduled                True
Volumes:
  kube-api-access-h7rtw:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  42m   default-scheduler  Successfully assigned default/kubernetes-app-manual to multinode-demo-m02
  Normal  Pulled     42m   kubelet            Container image "kmi8000/kubernetes_multi:0.2" already present on machine
  Normal  Created    41m   kubelet            Created container: kubernetes-app-image
  Normal  Started    41m   kubelet            Started container kubernetes-app-image
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> 
```

As can be seen the images are different 

```
IPs:
  IP:           10.244.0.3
Controlled By:  ReplicaSet/kubernetes-6c85f7555c
Containers:
  kubernetes-app:
    Container ID:   docker://3cd6ad8f7ac761763e0938b63f319ee53cc467fc569eb7c714031dcab9c1c039
    Image:          kmi8000/kubernetes_multi:0.1
```

```
IPs:
  IP:  10.244.1.5
Containers:
  kubernetes-app-image:
    Container ID:   docker://e0fc7600c0b720ce8f163636140e61b7720e06d1879b4ca2f570844112743281
    Image:          kmi8000/kubernetes_multi:0.2
```

Now we are sure, about the images let's proceed for the next step.

Open the `endpoints-service.yaml` file and add the IP addresses to the manifest file.

So it should look like this:

```
apiVersion: v1
kind: Service
metadata:
  name: endpoints-service
spec:
  ports:
  - port: 80
---
apiVersion: v1
kind: Endpoints
metadata:
  name: endpoints-service
subsets:
  - addresses:
    - ip: 10.244.1.5
    - ip: 10.244.0.3
    ports:
    - port: 8000
```
The name of Service `name: endpoints-service` and Endpoints `name: endpoints-service` are the same, the refore both of these pods will be registered to the endpoints-service Service.

Let's apply the `endpoints-service.yaml` manifest `kubectl apply -f .\endpoints-service.yaml` and check the services and endpoints that we have.

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl apply -f .\endpoints-service.yaml
service/endpoints-service created
endpoints/endpoints-service created

PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl get svc      
NAME                            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
endpoints-service               ClusterIP   10.109.42.136   <none>        80/TCP           62s
kubernetes                      ClusterIP   10.96.0.1       <none>        443/TCP          9h
kubernetes-app-manual-service   ClusterIP   10.110.174.90   <none>        80/TCP,443/TCP   52m
kubernetes-service              ClusterIP   10.101.171.99   <none>        80/TCP           5h50m

PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl get endpoints
NAME                            ENDPOINTS                                         AGE
endpoints-service               10.244.1.5:8000,10.244.0.3:8000                   71s
kubernetes                      192.168.49.2:8443                                 9h
kubernetes-app-manual-service   10.244.1.5:8000,10.244.1.5:8000                   52m
kubernetes-service              10.244.0.3:8000,10.244.1.2:8000,10.244.1.3:8000   5h51m
```

From the outputs of the these commands, we can see that the new service is running, and that the pods we had the IP addresses we assigned to the pods.

If we login to any pod and apply `curl` command towards the ClusterIP address of `endpoints-service` service, we will recieve the responses from each of the pods with different Docker images running on them

```
PS H:\GitHub\k8s\12. Service in Kubernetes - Part 1. Type ClusterIP Endpoints> kubectl exec -it kubernetes-6c85f7555c-wr676 -- bin/bash
root@kubernetes-6c85f7555c-wr676:/# curl http://10.109.42.136
Version 0.2
Hello world from hostname: kubernetes-app-manualroot@kubernetes-6c85f7555c-wr676:/# curl http://10.109.42.136
Hello world from hostname: kubernetes-6c85f7555c-zfwfzroot@kubernetes-6c85f7555c-wr676:/# curl http://10.109.42.136
Hello world from hostname: kubernetes-6c85f7555c-zfwfzroot@kubernetes-6c85f7555c-wr676:/# curl http://10.109.42.136
Hello world from hostname: kubernetes-6c85f7555c-zfwfzroot@kubernetes-6c85f7555c-wr676:/# curl http://10.109.42.136
Version 0.2
Hello world from hostname: kubernetes-app-manualroot@kubernetes-6c85f7555c-wr676:/#
```

By this example, we can see how does the Endpoints are working under the hood.