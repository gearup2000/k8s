# Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service.

Clean up all previously created services and deployments.

# Headless Service

First, let's copy the manifest files `kubernetes-deployment.yaml` and `clusterip-service.yaml` from previous part, and apply them.

```
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl apply -f .\kubernetes-deployment.yaml
deployment.apps/kubernetes created
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl apply -f .\clusterip-service.yaml  
service/kubernetes-service created
```

After deploying is that let's login to one of the pods, to see that the service `clusterip-service` works as expected. At the same time, let's install dnsutils by applying `apt update` and `apt-get install dnsutils`, since we will need them later.

**Installing dnsutils:**

```
root@kubernetes-6c85f7555c-8q4qf:/# apt update
Get:1 http://deb.debian.org/debian buster InRelease [122 kB]
Get:2 http://security.debian.org/debian-security buster/updates InRelease [34.8 kB]
Get:3 http://deb.debian.org/debian buster-updates InRelease [56.6 kB]
Get:4 http://security.debian.org/debian-security buster/updates/main amd64 Packages [610 kB]
Get:5 http://deb.debian.org/debian buster/main amd64 Packages [7909 kB]
Get:6 http://deb.debian.org/debian buster-updates/main amd64 Packages [8788 B]
Fetched 8741 kB in 1s (6594 kB/s)
Reading package lists... Done
Building dependency tree     
Reading state information... Done
199 packages can be upgraded. Run 'apt list --upgradable' to see them.
root@kubernetes-6c85f7555c-8q4qf:/# apt-get install dnsutils
Reading package lists... Done
Building dependency tree     
Reading state information... Done
The following additional packages will be installed:
  bind9-host geoip-database libbind9-161 libdns1104 libfstrm0 libgeoip1 libirs161 libisc1100 libisccc161 libisccfg163 libjson-c3 liblmdb0 liblwres161 libprotobuf-c1
Suggested packages:
  rblcheck geoip-bin
The following NEW packages will be installed:
  bind9-host dnsutils geoip-database libbind9-161 libdns1104 libfstrm0 libgeoip1 libirs161 libisc1100 libisccc161 libisccfg163 libjson-c3 liblmdb0 liblwres161 libprotobuf-c1
0 upgraded, 15 newly installed, 0 to remove and 199 not upgraded.
Need to get 6222 kB of archives.
After this operation, 17.9 MB of additional disk space will be used.
Do you want to continue? [Y/n] y
Get:1 http://security.debian.org/debian-security buster/updates/main amd64 libisc1100 amd64 1:9.11.5.P4+dfsg-5.1+deb10u11 [460 kB]
Get:2 http://deb.debian.org/debian buster/main amd64 libfstrm0 amd64 0.4.0-1 [20.8 kB]
Get:3 http://deb.debian.org/debian buster/main amd64 libgeoip1 amd64 1.6.12-1 [93.1 kB]
Get:4 http://deb.debian.org/debian buster/main amd64 libjson-c3 amd64 0.12.1+ds-2+deb10u1 [27.3 kB]
Get:5 http://deb.debian.org/debian buster/main amd64 liblmdb0 amd64 0.9.22-1 [45.0 kB]
Get:6 http://deb.debian.org/debian buster/main amd64 libprotobuf-c1 amd64 1.3.1-1+b1 [26.5 kB]
Get:7 http://deb.debian.org/debian buster/main amd64 geoip-database all 20181108-1 [2449 kB]
Get:8 http://security.debian.org/debian-security buster/updates/main amd64 libdns1104 amd64 1:9.11.5.P4+dfsg-5.1+deb10u11 [1217 kB]
Get:9 http://security.debian.org/debian-security buster/updates/main amd64 libisccc161 amd64 1:9.11.5.P4+dfsg-5.1+deb10u11 [238 kB]
Get:10 http://security.debian.org/debian-security buster/updates/main amd64 libisccfg163 amd64 1:9.11.5.P4+dfsg-5.1+deb10u11 [268 kB]
Get:11 http://security.debian.org/debian-security buster/updates/main amd64 libbind9-161 amd64 1:9.11.5.P4+dfsg-5.1+deb10u11 [247 kB]
Get:12 http://security.debian.org/debian-security buster/updates/main amd64 liblwres161 amd64 1:9.11.5.P4+dfsg-5.1+deb10u11 [252 kB]
Get:13 http://security.debian.org/debian-security buster/updates/main amd64 bind9-host amd64 1:9.11.5.P4+dfsg-5.1+deb10u11 [272 kB]
Get:14 http://security.debian.org/debian-security buster/updates/main amd64 libirs161 amd64 1:9.11.5.P4+dfsg-5.1+deb10u11 [239 kB]
Get:15 http://security.debian.org/debian-security buster/updates/main amd64 dnsutils amd64 1:9.11.5.P4+dfsg-5.1+deb10u11 [366 kB]
Fetched 6222 kB in 0s (41.7 MB/s)
debconf: delaying package configuration, since apt-utils is not installed
Selecting previously unselected package libfstrm0:amd64.
(Reading database ... 24604 files and directories currently installed.)
Preparing to unpack .../00-libfstrm0_0.4.0-1_amd64.deb ...
Unpacking libfstrm0:amd64 (0.4.0-1) ...
Selecting previously unselected package libgeoip1:amd64.
Preparing to unpack .../01-libgeoip1_1.6.12-1_amd64.deb ...
Unpacking libgeoip1:amd64 (1.6.12-1) ...
Selecting previously unselected package libjson-c3:amd64.
Preparing to unpack .../02-libjson-c3_0.12.1+ds-2+deb10u1_amd64.deb ...
Unpacking libjson-c3:amd64 (0.12.1+ds-2+deb10u1) ...
Selecting previously unselected package liblmdb0:amd64.
Preparing to unpack .../03-liblmdb0_0.9.22-1_amd64.deb ...
Unpacking liblmdb0:amd64 (0.9.22-1) ...
Selecting previously unselected package libprotobuf-c1:amd64.
Preparing to unpack .../04-libprotobuf-c1_1.3.1-1+b1_amd64.deb ...
Unpacking libprotobuf-c1:amd64 (1.3.1-1+b1) ...
Selecting previously unselected package libisc1100:amd64.
Preparing to unpack .../05-libisc1100_1%3a9.11.5.P4+dfsg-5.1+deb10u11_amd64.deb ...
Unpacking libisc1100:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Selecting previously unselected package libdns1104:amd64.
Preparing to unpack .../06-libdns1104_1%3a9.11.5.P4+dfsg-5.1+deb10u11_amd64.deb ...
Unpacking libdns1104:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Selecting previously unselected package libisccc161:amd64.
Preparing to unpack .../07-libisccc161_1%3a9.11.5.P4+dfsg-5.1+deb10u11_amd64.deb ...
Unpacking libisccc161:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Selecting previously unselected package libisccfg163:amd64.
Preparing to unpack .../08-libisccfg163_1%3a9.11.5.P4+dfsg-5.1+deb10u11_amd64.deb ...
Unpacking libisccfg163:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Selecting previously unselected package libbind9-161:amd64.
Preparing to unpack .../09-libbind9-161_1%3a9.11.5.P4+dfsg-5.1+deb10u11_amd64.deb ...
Unpacking libbind9-161:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Selecting previously unselected package liblwres161:amd64.
Preparing to unpack .../10-liblwres161_1%3a9.11.5.P4+dfsg-5.1+deb10u11_amd64.deb ...
Unpacking liblwres161:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Selecting previously unselected package bind9-host.
Preparing to unpack .../11-bind9-host_1%3a9.11.5.P4+dfsg-5.1+deb10u11_amd64.deb ...
Unpacking bind9-host (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Selecting previously unselected package libirs161:amd64.
Preparing to unpack .../12-libirs161_1%3a9.11.5.P4+dfsg-5.1+deb10u11_amd64.deb ...
Unpacking libirs161:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Selecting previously unselected package dnsutils.
Preparing to unpack .../13-dnsutils_1%3a9.11.5.P4+dfsg-5.1+deb10u11_amd64.deb ...
Unpacking dnsutils (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Selecting previously unselected package geoip-database.
Preparing to unpack .../14-geoip-database_20181108-1_all.deb ...
Unpacking geoip-database (20181108-1) ...
Setting up liblmdb0:amd64 (0.9.22-1) ...
Setting up libjson-c3:amd64 (0.12.1+ds-2+deb10u1) ...
Setting up libfstrm0:amd64 (0.4.0-1) ...
Setting up libprotobuf-c1:amd64 (1.3.1-1+b1) ...
Setting up libgeoip1:amd64 (1.6.12-1) ...
Setting up geoip-database (20181108-1) ...
Setting up libisc1100:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Setting up liblwres161:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Setting up libisccc161:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Setting up libdns1104:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Setting up libisccfg163:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Setting up libbind9-161:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Setting up libirs161:amd64 (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Setting up bind9-host (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Setting up dnsutils (1:9.11.5.P4+dfsg-5.1+deb10u11) ...
Processing triggers for libc-bin (2.28-10) ...
```

**Checking `clusterip-service` service:**

```
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
kubernetes-6c85f7555c-8q4qf   1/1     Running   0          2m55s
kubernetes-6c85f7555c-9wrvx   1/1     Running   0          2m55s
kubernetes-6c85f7555c-lrb4p   1/1     Running   0          2m55s
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl exec -it kubernetes-6c85f7555c-8q4qf -- bin/bash
root@kubernetes-6c85f7555c-8q4qf:/# curl http://kubernetes-service
Hello world from hostname: kubernetes-6c85f7555c-lrb4proot@kubernetes-6c85f7555c-8q4qf:/# curl http://kubernetes-service
Hello world from hostname: kubernetes-6c85f7555c-9wrvxroot@kubernetes-6c85f7555c-8q4qf:/# curl http://kubernetes-service
Hello world from hostname: kubernetes-6c85f7555c-8q4qfroot@kubernetes-6c85f7555c-8q4qf:/# curl http://kubernetes-service
root@kubernetes-6c85f7555c-8q4qf:/# exit
exit
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> 
```

As can be seen, we got responces from each pods (see the middle part of the responces `kubernetes-6c85f7555c-lrb4proot`, `kubernetes-6c85f7555c-9wrvxroot` and `kubernetes-6c85f7555c-8q4qfroot`).

However, sometimes we need to bypass this kind of behaviour of service, and send a message to all pods simultaneously.
This can be achieved by using Headless service. This service has ClusterIP settings set as `None`, and operates with `selector` instead. Let's look at the example below. The selector labels are set to `app=http-server` just like in `kubernetes-deployment.yaml` and `kubernetes-clusterip-service.yaml` respectively.

```
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-headless-service
spec:
  clusterIP: None
  selector:
    app: http-server
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  clusterIP: None
  type: ClusterIP
```

let's create a `headless-clusterip-service.yaml` file out of the example, apply it and check the services we had.

```
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl apply -f .\headless-clusterip-service.yaml
service/kubernetes-headless-service created
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl get svc                                       
NAME                          TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
kubernetes                    ClusterIP   10.96.0.1      <none>        443/TCP   30h
kubernetes-headless-service   ClusterIP   None           <none>        80/TCP    9m39s
kubernetes-service            ClusterIP   10.101.151.7   <none>        80/TCP    92m
```

As can be seen from the the output, we have `kubernetes-headless-service` which have no ClusterIP at all.

let's login back to the pod and check the `headless-clusterip-service`.

```
root@kubernetes-6c85f7555c-8q4qf:/# curl http://kubernetes-service
Hello world from hostname: kubernetes-6c85f7555c-9wrvxroot@kubernetes-6c85f7555c-8q4qf:/# ^C
root@kubernetes-6c85f7555c-8q4qf:/# curl http://kubernetes-headless-service
curl: (7) Failed to connect to kubernetes-headless-service port 80: Connection refused
root@kubernetes-6c85f7555c-8q4qf:/# nslookup kubernetes-headless-service
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   kubernetes-headless-service.default.svc.cluster.local
Address: 10.244.1.5
Name:   kubernetes-headless-service.default.svc.cluster.local
Address: 10.244.1.6
Name:   kubernetes-headless-service.default.svc.cluster.local
Address: 10.244.0.4

root@kubernetes-6c85f7555c-8q4qf:/# nslookup kubernetes-headless-service:8000
Server:         10.96.0.10
Address:        10.96.0.10#53

root@kubernetes-6c85f7555c-8q4qf:/# curl kubernetes-headless-service:8000
Hello world from hostname: kubernetes-6c85f7555c-8q4qfroot@kubernetes-6c85f7555c-8q4qf:/#
```

As can be determined from the outputs, even the `headless-clusterip-service` has no ClusterIP address, we still able to use its DNS record of it, but the responces are comming directly from the pods.
We also can use `curl` command, in that case we will get responce from one pod that is behind of the `headless-clusterip-service` service.

```
root@kubernetes-6c85f7555c-8q4qf:/# curl kubernetes-headless-service:8000
Hello world from hostname: kubernetes-6c85f7555c-8q4qfroot@kubernetes-6c85f7555c-8q4qf:/#
```

So, in case we have some third side application that is need to be connected to ALL pods simultaneously, we can use `headless-clusterip-service` method.

Let's remove these `clusterip-service` and `headless-clusterip-service` services.

```
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl delete -f .\headless-clusterip-service.yaml
service "kubernetes-headless-service" deleted
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl delete -f .\clusterip-service.yaml       
service "kubernetes-service" deleted
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   31h
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> 
```

# ExternalName service

let's create a new manifest file calling `externalname-service.yaml` which will have the following properties:

```
apiVersion: v1
kind: Service
metadata:
  name: external-service
spec:
  type: ExternalName
  externalName: example.com
```

This kind of service is using in case we need to connect for example to the remote database.
As we already know our pods can communicate by DNS records. Since the DNS name of particular service will stay the same, we could change the `externalName` value. Let's say the database name has been changed from `database1.someDNSrecord.com` to `database2.someDNSrecord.com`, then all we need it's to change the name to the new one, and re-apply the manifest file.
As can be seen below the manifest file has no selector part, and basically just creates a CNAME DNS record of example.com address.

Let's apply the manifest `externalname-service` file and check the services list.

```
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl apply -f .\externalname-service.yaml
service/external-service created
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl get svc
NAME               TYPE           CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
external-service   ExternalName   <none>       example.com   <none>    3m1s
kubernetes         ClusterIP      10.96.0.1    <none>        443/TCP   31h
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> 
```

As can been found in the output, we again have no ClusterIP on newly created `external-service` service.

Now let's login back to the one of the pods, and check what we get when we apply `nslookup` command towards the `external-service` dns records.

```
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl exec -it kubernetes-6c85f7555c-8q4qf -- bin/bash
root@kubernetes-6c85f7555c-8q4qf:/#
root@kubernetes-6c85f7555c-8q4qf:/# nslookup external-service
Server:         10.96.0.10                                                                                                                                                        
Address:        10.96.0.10#53

external-service.default.svc.cluster.local      canonical name = example.com.
Name:   example.com
Address: 96.7.128.175
Name:   example.com
Address: 23.192.228.80
Name:   example.com
Address: 23.215.0.136
Name:   example.com
Address: 23.215.0.138
Name:   example.com
Address: 96.7.128.198
Name:   example.com
Address: 23.192.228.84
Name:   example.com
Address: 2600:1406:3a00:21::173e:2e66
Name:   example.com
Address: 2600:1406:bc00:53::b81e:94c8
Name:   example.com
Address: 2600:1408:ec00:36::1736:7f24
Name:   example.com
Address: 2600:1406:bc00:53::b81e:94ce
Name:   example.com
Address: 2600:1406:3a00:21::173e:2e65
Name:   example.com
Address: 2600:1408:ec00:36::1736:7f31
```

As the output shows, the external name is `example.com` the list of public IP addresses, and we have created a CNAME `external-service.default.svc.cluster.local` to the `example.com` address.
The externalName service works with DNS records.

**Warning!!!**

The ExternalName service strugles with HTTP and HTTPS protocol support.

As Kubernetes documentation says in the following [link](https://kubernetes.io/docs/concepts/services-networking/service/#:~:text=Caution%3A,client%20connected%20to.https:/) 

```
**Caution:**
You may have trouble using ExternalName for some common protocols, including HTTP and HTTPS. If you use ExternalName then the hostname used by clients inside your cluster is different from the name that the ExternalName references.

For protocols that use hostnames this difference may lead to errors or unexpected responses. HTTP requests will have a Host: header that the origin server does not recognize; TLS servers will not be able to provide a certificate matching the hostname that the client connected to.
```

Let's now remove the `external_name` service and continue with the NodePort and LoadBalancer services.

```
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl delete -f .\externalname-service.yaml
service "external-service" deleted
```

# NodePort

In case we need to access the cluster from outside we can use the NodePort or LoadBalancer services.

Let's create a manifest file calling `nodeport-service.yaml` with the following properties:

```
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-service-nodeport
spec:
  #externalTrafficPolicy: Local
  #sessionsAffinity: ClientIP
  selector:
    app: http-server
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
      #nodePort: 30080 # port-range: 30000-32767
  type: NodePort
```

As can be seen below, there is a part calling nodePort but it is commented out because Kubernetes can pick the port according to the availability of the port range.
But the port can be specified in case we need some specific port, and the port must be well documented so there is no overlapping with another services.

A NodePort service is the most basic way to get external traffic directly to your service. NodePort, as the name implies, opens a specific port, and any traffic that is sent to this port is forwarded to the service.

In case we would have deployed our cluster in Cloud, for example GCP, AWS or azure, we would have the External IP showining after apply the command `kubectl get svc`.
Since we are running our cluster locally, and uding minikube, the `kubectl get svc` return the table with values as `none` for External IP,

```
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl get svc
NAME                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes                    ClusterIP   10.96.0.1       <none>        443/TCP        2d9h
kubernetes-service-nodeport   NodePort    10.110.64.183   <none>        80:30080/TCP   18h
```

However, we can use the following command  `minikube service kubernetes-service-nodeport --url`. This will create a s tunnel.
The command exposes the service directly to any program running on the host operating system.

```
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> minikube service kubernetes-service-nodeport --url
http://127.0.0.1:50789
❗  Because you are using a Docker driver on windows, the terminal needs to be open to run it.
```
Let's open a new terminal and and apply `curl http://127.0.0.1:50789` command to check that we are getting responces from our pods:

```
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> curl http://127.0.0.1:50789


StatusCode        : 200
StatusDescription : OK
Content           : {72, 101, 108, 108...}                                                                                                                                                             RawContent        : HTTP/1.0 200 OK                                                                                                                                                                                        Date: Tue, 11 Mar 2025 01:26:49 GMT                                                                                                                                                                    Server: BaseHTTP/0.6 Python/3.8.5                                                                                                                                                  

                    Hello world from hostname: kubernetes-6c85f7555c-9wrvx
Headers           : {[Date, Tue, 11 Mar 2025 01:26:49 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 54



PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> curl http://127.0.0.1:50789


StatusCode        : 200
StatusDescription : OK
Content           : {72, 101, 108, 108...}
RawContent        : HTTP/1.0 200 OK
                    Date: Tue, 11 Mar 2025 01:26:59 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5

                    Hello world from hostname: kubernetes-6c85f7555c-8q4qf
Headers           : {[Date, Tue, 11 Mar 2025 01:26:59 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 54



PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> curl http://127.0.0.1:50789


StatusCode        : 200
StatusDescription : OK
Content           : {72, 101, 108, 108...}
RawContent        : HTTP/1.0 200 OK
                    Date: Tue, 11 Mar 2025 01:27:02 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5

                    Hello world from hostname: kubernetes-6c85f7555c-lrb4p
Headers           : {[Date, Tue, 11 Mar 2025 01:27:02 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 54



PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> 
```
It can be confused when you see that when you run `minikube service <service-name> --url`, there is different portnumbers. To understand this let's see how does the `minikube service <service-name> --url` works:

 The Minikube does the following:
a. It identifies the NodePort that Kubernetes assigned to your service.
b. It creates a network tunnel between your host machine and the Minikube VM.
c. It maps a port on your localhost (127.0.0.1) to the NodePort of your service in the Minikube VM.
d. Port Forwarding: The tunnel essentially performs port forwarding. It takes requests from a randomly assigned port on your localhost and forwards them to the NodePort of your service in the Minikube cluster.
e. Dynamic Port Assignment: The port on your localhost is dynamically assigned. This is why you see a different port number (like 50789 in your example) each time you run the command.



In case the cluster is deployed on a cloud provider we would use the External IP address and port we have configured in manifest file.

For example:

```
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl get nodes -o wide
NAME                 STATUS   ROLES           AGE    VERSION   INTERNAL-IP    EXTERNAL-IP           OS-IMAGE             KERNEL-VERSION                       CONTAINER-RUNTIME
multinode-demo       Ready    control-plane   2d9h   v1.32.0   192.168.49.2   15.237.144.183        Ubuntu 22.04.5 LTS   5.15.167.4-microsoft-standard-WSL2   docker://27.4.1
multinode-demo-m02   Ready    <none>          2d9h   v1.32.0   192.168.49.3   35.181.26.237         Ubuntu 22.04.5 LTS   5.15.167.4-microsoft-standard-WSL2   docker://27.4.1
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> curl http://15.237.144.183:30080

StatusCode        : 200
StatusDescription : OK
Content           : {72, 101, 108, 108...}
RawContent        : HTTP/1.0 200 OK
                    Date: Tue, 11 Mar 2025 01:26:49 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5                                                                                                                                                  

                    Hello world from hostname: kubernetes-6c85f7555c-9wrvx
Headers           : {[Date, Tue, 11 Mar 2025 01:26:49 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 54
```

**The important part of NodePort service, when we apply the service NodePort we do expose the disared (or assigned by Kubernetes) port on ALL pods.**

## sessionsAffinity

In case we would like to stick the session from client to a disered pod, we could use the sessionAffinity.

The traffic from the same client IP address will be forwarded to the same pod.


# LoadBalancer

A LoadBalancer service in Kubernetes is used to expose your application to external traffic. It automatically provisions an external IP address that can be used to access the service from outside the Kubernetes cluster. This type of service is typically used in cloud environments where the cloud provider can provision a load balancer for you.

### How LoadBalancer Service Works

1. **Service Definition**: You define a LoadBalancer service in a YAML file, specifying the ports and selectors.
2. **Provisioning**: When you apply the service definition, Kubernetes communicates with the cloud provider to provision a load balancer.
3. **External IP**: The cloud provider assigns an external IP address to the load balancer.
4. **Traffic Routing**: The load balancer routes incoming traffic to the service, which then forwards it to the appropriate pods based on the selectors.


The Key Points of LoadBalancer Definition:

- **Automatic Provisioning**: The cloud provider automatically provisions a load balancer and assigns an external IP address.
- **External Traffic**: The LoadBalancer service is used to expose your application to external traffic.
- **Cloud Provider Integration**: This type of service is typically used in cloud environments (e.g., AWS, GCP, Azure) where the cloud provider can provision a load balancer.

### Example of LoadBalancer Service

Here is an example of a LoadBalancer service definition that we will use to configure our minikube cluster, let's name it as `lb-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-service-lb
spec:
  selector:
    app: http-server
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

Applying the LoadBalancer Service by `kubectl apply -f lb-service.yaml`, since we are using the minikube the status of ExternalIP will be pending, but we can use `minikube tunnel` to emulate the ExternalIP. To do so run `minikube tunnel` in separate terminal.

```sh
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl get svc kubernetes-service-lb      
NAME                    TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes-service-lb   LoadBalancer   10.100.72.156   <pending>     80:30125/TCP   17s
H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl get svc kubernetes-service-lb
NAME                    TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes-service-lb   LoadBalancer   10.100.72.156   127.0.0.1     80:30125/TCP   3m16s
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> 
```

### Accessing the Service

Once the LoadBalancer service is created and an external IP address is assigned, you can access your application using the external IP address and the specified port:

```sh
curl http://127.0.0.1:80
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> curl http://127.0.0.1:80


StatusCode        : 200
StatusDescription : OK
Content           : {72, 101, 108, 108...}                                                                                                                       RawContent        : HTTP/1.0 200 OK                                                                                                                                                  Date: Wed, 12 Mar 2025 09:15:28 GMT                                                                                                                              Server: BaseHTTP/0.6 Python/3.8.5                                                                                                            

                    Hello world from hostname: kubernetes-6c85f7555c-8q4qf
Headers           : {[Date, Wed, 12 Mar 2025 09:15:28 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 54



PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> curl http://127.0.0.1:80


StatusCode        : 200
StatusDescription : OK
Content           : {72, 101, 108, 108...}
RawContent        : HTTP/1.0 200 OK
                    Date: Wed, 12 Mar 2025 09:15:32 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5

                    Hello world from hostname: kubernetes-6c85f7555c-lrb4p
Headers           : {[Date, Wed, 12 Mar 2025 09:15:32 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 54



PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> curl http://127.0.0.1:80


StatusCode        : 200
StatusDescription : OK
Content           : {72, 101, 108, 108...}
RawContent        : HTTP/1.0 200 OK
                    Date: Wed, 12 Mar 2025 09:15:35 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5

                    Hello world from hostname: kubernetes-6c85f7555c-9wrvx
Headers           : {[Date, Wed, 12 Mar 2025 09:15:35 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 54



PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> 
```

As can be seen from the `curl` outputs we are getting the responces from each pods. If we apply the `kubectl get pods -o wide` we can see that pods are deployed in two separate nodes. 

```sh
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl get pods -o wide
NAME                          READY   STATUS    RESTARTS      AGE     IP           NODE                 NOMINATED NODE   READINESS GATES
kubernetes-6c85f7555c-8q4qf   1/1     Running   4 (27m ago)   2d12h   10.244.1.5   multinode-demo-m02   <none>           <none>
kubernetes-6c85f7555c-9wrvx   1/1     Running   4 (27m ago)   2d12h   10.244.1.3   multinode-demo-m02   <none>           <none>
kubernetes-6c85f7555c-lrb4p   1/1     Running   4 (28m ago)   2d12h   10.244.0.2   multinode-demo       <none>           <none>
```

The loadbalancer-service has randomly chosen the port and exposed it in each pods we have, to see what port is it we can apply command as `kubectl describe service kubernetes-service-lb`

```sh
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> kubectl describe service kubernetes-service-lb      
Name:                     kubernetes-service-lb
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 app=http-server
Type:                     LoadBalancer
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.100.72.156
IPs:                      10.100.72.156
LoadBalancer Ingress:     127.0.0.1 (VIP)
Port:                     <unset>  80/TCP
TargetPort:               8000/TCP
NodePort:                 <unset>  30125/TCP
Endpoints:                10.244.1.5:8000,10.244.0.2:8000,10.244.1.3:8000
Session Affinity:         None
External Traffic Policy:  Cluster
Internal Traffic Policy:  Cluster
Events:                   <none>
PS H:\GitHub\k8s\13. Service in Kubernetes - Part 2. Types-ExternalName, NodePort and LoadBalancer. Headless Service> 
```

As can be seen in the output of the described command above the port number is `30125`.

### Traffic Distribution

- **Pods**: The LoadBalancer service distributes incoming traffic among the pods that match the service's selector. This ensures that the load is balanced across all available pods.
- **Nodes**: While the load balancer itself may be aware of the nodes, the primary focus is on distributing traffic to the pods. The underlying nodes hosting these pods are not directly targeted by the load balancer.

However, sometimes the port on Node cannot be determined, misconfigured or otherwise invalid. In this case, we can send the traffic directly to the nodes where the pods are running, without being forwarded to other nodes. To achive that we can add settings as `externalTrafficPolicy: Local`. This allows us to control the traffic to the nodes where the pods are running.

The key points of this approach are:

- **Preserves Source IP**: The client’s source IP address is preserved and made available to the backend pods.
- **Direct Routing**: Traffic is routed directly to the nodes where the pods are running, without being forwarded to other nodes.
- **Potential Imbalance**: If the pods are not evenly distributed across the nodes, this can lead to an imbalance in traffic distribution.

Also, setting `externalTrafficPolicy` to `Local` is particularly useful in scenarios where you need to preserve the client’s source IP address for logging, auditing, or other purposes. It ensures that the backend pods can see the original source IP address of the client.

The second option is `externalTrafficPolicy: Cluster`.

### Comparison with `externalTrafficPolicy: Cluster`

- **Cluster**: Traffic is routed to any node in the cluster, and then forwarded to the appropriate pods. This can lead to better load distribution but does not preserve the client’s source IP address.
- **Local**: Traffic is routed only to the nodes where the target pods are running, preserving the client’s source IP address but potentially leading to an imbalance in traffic distribution if the pods are not evenly distributed.


