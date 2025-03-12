# 14. Ingress in Kubernetes. Creating ingress on Minikube

The services of kubernetes are workinng on transport layer 4 of OSI model which means they works with TCP and UDP protocols.
The LoadBalancer service is providing by cloud provider, the refore cannot be deployed locally. Also, the cost of cloud based load balancer is usually expensive.

The Kubernetes has also a service calling Ingress which works on layer 7 of OSI model.
The layer 7 of OSI model operates with HTTP/HTTPS, SMTP, FTP, SSH, DNS protocols, which gives the functionality for example sticking sessions, inspects messages, and make routing decisions based on they content etc..

To make the Ingress service work, the so called Ingress Controller must be deployed.

Let's start building the new cluster and see what is the Ingress.

Deploy a cluster with single nod `minikube start`.
Check the pods of all namespaces `kubectl get pods --all-namespaces`.
Apply watch command in separated second terminal, to see what services will be deployed `kubectl get pods --all-namespaces --watch`.
Go back to the first terminal and run `minikube addons list` to see what built-in services are available by Minikube, and activate the services we will need.

```bash
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> minikube addons list
|-----------------------------|----------|--------------|--------------------------------|
|         ADDON NAME          | PROFILE  |    STATUS    |           MAINTAINER           |
|-----------------------------|----------|--------------|--------------------------------|
| ambassador                  | minikube | disabled     | 3rd party (Ambassador)         |
| amd-gpu-device-plugin       | minikube | disabled     | 3rd party (AMD)                |
| auto-pause                  | minikube | disabled     | minikube                       |
| cloud-spanner               | minikube | disabled     | Google                         |
| csi-hostpath-driver         | minikube | disabled     | Kubernetes                     |
| dashboard                   | minikube | disabled     | Kubernetes                     |
| default-storageclass        | minikube | enabled ✅   | Kubernetes                     |
| efk                         | minikube | disabled     | 3rd party (Elastic)            |
| freshpod                    | minikube | disabled     | Google                         |
| gcp-auth                    | minikube | disabled     | Google                         |
| gvisor                      | minikube | disabled     | minikube                       |
| headlamp                    | minikube | disabled     | 3rd party (kinvolk.io)         |
| inaccel                     | minikube | disabled     | 3rd party (InAccel             |
|                             |          |              | [info@inaccel.com])            |
| ingress                     | minikube | disabled     | Kubernetes                     |
| ingress-dns                 | minikube | disabled     | minikube                       |
| inspektor-gadget            | minikube | disabled     | 3rd party                      |
|                             |          |              | (inspektor-gadget.io)          |
| istio                       | minikube | disabled     | 3rd party (Istio)              |
| istio-provisioner           | minikube | disabled     | 3rd party (Istio)              |
| kong                        | minikube | disabled     | 3rd party (Kong HQ)            |
| kubeflow                    | minikube | disabled     | 3rd party                      |
| kubevirt                    | minikube | disabled     | 3rd party (KubeVirt)           |
| logviewer                   | minikube | disabled     | 3rd party (unknown)            |
| metallb                     | minikube | disabled     | 3rd party (MetalLB)            |
| metrics-server              | minikube | disabled     | Kubernetes                     |
| nvidia-device-plugin        | minikube | disabled     | 3rd party (NVIDIA)             |
| nvidia-driver-installer     | minikube | disabled     | 3rd party (NVIDIA)             |
| nvidia-gpu-device-plugin    | minikube | disabled     | 3rd party (NVIDIA)             |
| olm                         | minikube | disabled     | 3rd party (Operator Framework) |
| pod-security-policy         | minikube | disabled     | 3rd party (unknown)            |
| portainer                   | minikube | disabled     | 3rd party (Portainer.io)       |
| registry                    | minikube | disabled     | minikube                       |
| registry-aliases            | minikube | disabled     | 3rd party (unknown)            |
| registry-creds              | minikube | disabled     | 3rd party (UPMC Enterprises)   |
| storage-provisioner         | minikube | enabled ✅   | minikube                       |
| storage-provisioner-gluster | minikube | disabled     | 3rd party (Gluster)            |
| storage-provisioner-rancher | minikube | disabled     | 3rd party (Rancher)            |
| volcano                     | minikube | disabled     | third-party (volcano)          |
| volumesnapshots             | minikube | disabled     | Kubernetes                     |
| yakd                        | minikube | disabled     | 3rd party (marcnuri.com)       |
|-----------------------------|----------|--------------|--------------------------------|
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> 
```

We need to Enable the Ingress addon, by apllying `minikube addons enable ingress` command. Check second terminal to see that 2 `ingress-nginx-controller-<some-id> are in running state.

```
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> kubectl get pods --all-namespaces --watch
NAMESPACE     NAME                               READY   STATUS    RESTARTS      AGE
output ommited...
ingress-nginx   ingress-nginx-controller-56d7c84fd4-svqtp   0/1     Running             0             32s
ingress-nginx   ingress-nginx-controller-56d7c84fd4-svqtp   1/1     Running             0             44s
```

Before we deploy any ingress resource, let's check that we do not have any.

```
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> kubectl get ingresses --all-namespaces 
No resources found
```

Let's now deploy the manifest files `deploy-svc-app-latest.yaml`, `deploy-svc-app-v1.yaml`, `deploy-svc-app-v2.yaml` and `deploy-svc-app-v3.yaml`.

```bash
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> kubectl.exe apply -f .\deploy-svc-app-latest.yaml -f .\deploy-svc-app-v1.yaml -f .\deploy-svc-app-v2.yaml -f .\deploy-svc-app-v3.yaml
deployment.apps/kubernetes created
service/kubernetes-service created
deployment.apps/kubernetes-v1 created
service/kubernetes-service-v1 created
deployment.apps/kubernetes-v2 created
service/kubernetes-service-v2 created
deployment.apps/kubernetes-v3 created
service/kubernetes-service-v3 created
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> 
```

Check the deployments configuration.

```bash
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> kubectl get deployment -o wide
NAME            READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS       IMAGES                         SELECTOR
kubernetes      2/2     1            2           2m7s   kubernetes-app   kmi8000/kubernetes_multi       app=http-server
kubernetes-v1   2/2     2            2           2m7s   kubernetes-app   kmi8000/kubernetes_multi:0.1   app=http-server-v1
kubernetes-v2   2/2     2            2           2m7s   kubernetes-app   kmi8000/kubernetes_multi:0.2   app=http-server-v2
kubernetes-v3   2/2     2            2           2m7s   kubernetes-app   kmi8000/kubernetes_multi:0.3   app=http-server-v3
```
So we have 4 deployments with 2 replicas each with 3 different versions.

Let's check that services are actually using the different versions of Docker images.

```bash
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> kubectl get pods -o wide      
NAME                             READY   STATUS             RESTARTS   AGE   IP            NODE       NOMINATED NODE   READINESS GATES
kubernetes-6c85f7555c-89qmm      1/1     Running            0          53m   10.244.0.10   minikube   <none>           <none>
kubernetes-6c85f7555c-gbn8m      1/1     Running            0          53m   10.244.0.6    minikube   <none>           <none>
kubernetes-944484756-8m56s       0/1     ImagePullBackOff   0          51m   10.244.0.14   minikube   <none>           <none>
kubernetes-v1-84cbd67567-7j4wh   1/1     Running            0          53m   10.244.0.9    minikube   <none>           <none>
kubernetes-v1-84cbd67567-ls8lk   1/1     Running            0          53m   10.244.0.8    minikube   <none>           <none>
kubernetes-v2-c88447579-5s7ft    1/1     Running            0          51m   10.244.0.16   minikube   <none>           <none>
kubernetes-v2-c88447579-jn8xz    1/1     Running            0          51m   10.244.0.15   minikube   <none>           <none>
kubernetes-v3-7bb97dbbf5-9dx9d   1/1     Running            0          53m   10.244.0.11   minikube   <none>           <none>
kubernetes-v3-7bb97dbbf5-wgvsl   1/1     Running            0          53m   10.244.0.12   minikube   <none>           <none>
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> kubectl get svc -o wide 
NAME                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE   SELECTOR
kubernetes              ClusterIP   10.96.0.1        <none>        443/TCP   71m   <none>
kubernetes-service      ClusterIP   10.97.32.152     <none>        80/TCP    54m   app=http-server
kubernetes-service-v1   ClusterIP   10.103.78.177    <none>        80/TCP    54m   app=http-server-v1
kubernetes-service-v2   ClusterIP   10.109.141.168   <none>        80/TCP    54m   app=http-server-v2
kubernetes-service-v3   ClusterIP   10.101.122.176   <none>        80/TCP    54m   app=http-server-v3
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> kubectl exec -it kubernetes-6c85f7555c-89qmm -- bin/bash
root@kubernetes-6c85f7555c-89qmm:/# curl http://kubernetes-service
Hello world from hostname: kubernetes-6c85f7555c-89qmmroot@kubernetes-6c85f7555c-89qmm:/# curl http://kubernetes-service-v1
Hello world from hostname: kubernetes-v1-84cbd67567-7j4whroot@kubernetes-6c85f7555c-89qmm:/# curl http://kubernetes-service-v2
Version 0.2
Hello world from hostname: kubernetes-v2-c88447579-jn8xzroot@kubernetes-6c85f7555c-89qmm:/# curl http://kubernetes-service-v3
Version 0.3
Hello world from hostname: kubernetes-v3-7bb97dbbf5-9dx9droot@kubernetes-6c85f7555c-89qmm:/#
```

Since the versions are correct let's check what do we have in `ingress.yaml` file:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
spec:
  rules:
   - host: app.example.com
     http:
        paths:
          - pathType: Prefix
            path: /
            backend:
              service:
                name: kubernetes-service
                port: 
                  number: 80
          - pathType: Prefix
            path: /v1
            backend:
              service:
                name: kubernetes-service-v1
                port: 
                  number: 80
          - pathType: Exact
            path: /v2
            backend:
              service:
                name: kubernetes-service-v2
                port: 
                  number: 80
   - host: app-v3.example.com
     http:
        paths:
          - pathType: Exact
            path: /
            backend:
              service:
                name: kubernetes-service-v3
                port: 
                  number: 80
```

The part `-host` tells that we want to create two hosts ``app.example.com` and `app-v3.example.com`
The part:
```yaml
              service:
                name: kubernetes-service-<version>
``` 
tells which service is responsable for forwarding traffic to the correct pods according to the requests.

1. For example, if the client will request the page `app.example.com` the traffic will be forwarded to the `kubernetes-service` service.

2. When the client will request the page `app.example.com/v1` the traffic will be forwarded to the service `kubernetes-service-v1`. **AND ALSO,** if the requested page will be `app.example.com/v1ANYTEXT` meaning any added text after the `/v1` the traffic will be forwarded to the `kubernetes-service-v1` and corresponding page will be opened. The reason is the `- pathType: Prefix` value, which means if the beggining part of the address is matching with the main condition, which is host `app.example.com` + Prefix `/v1`, then any added text will be ignored, and the `app.example.com/v1` page will ne opened. 
  Examples: `app.example.com/v1ANYTHPAGE` = `app.example.com/v1`,
            `app.example.com/v1I WANT TO OPEN OTHER PAGE` = `app.example.com/v1`.

3. When the client will try to open the page `app.example.com/v2`, the traffic will be forwarded to the service `kubernetes-service-v2`, and also the requested page must be exactly `app.example.com/v2`. Otherwise, the traffic will be forwarded to the host `app.example.com`.

4. When the client will try to open the page `app-v3.example.com`, the traffic will be forwarded to the service `kubernetes-service-v3`, and also the requested page must be exactly `app-v3.example.com`. Otherwise as a responce the clinet will get the error message.

Let's apply the `ingress.yaml` manifest and see what it will happen.

```bash
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> kubectl apply -f .\ingress.yaml
ingress.networking.k8s.io/main-ingress created
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> 
```
Now if will try to open addresses **app.example.com** and **app-v3.example.com** we will get 404 errors, this is because we are trying to open the websites of Internet, which does not exists. But they are available locally. To make them available, let's edit the hosts file of local machine.

First check what it the IP address of the Minikube by issueing the following command in the terminal:

```bash
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> minikube ip
192.168.58.2
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> 
```

After that follow the next steps:

**Windows-based:**

To find and edit the hosts file on a Windows-based machine, follow these steps:
1. Open File Explorer.
2. Navigate to: C:\Windows\System32\drivers\etc\
3. You should see a file named hosts without any file extension.
4. To edit this file, you'll need administrator privileges. Here's how to open it with elevated permissions:
   a. Right-click on Notepad in your Start menu.
   b. Select "Run as administrator".
   c. In Notepad, go to File > Open.
   d. Navigate to C:\Windows\System32\drivers\etc\
   e. In the file type dropdown, change it to "All Files (.)"
   f. Select the hosts file and click Open.
5. Now you can edit the file. Add your entries at the end of the file, for example:
```
   192.168.58.2    app.example.com
   192.168.58.2    app-v3.example.com
```
6. Save the file when you're done.

Unux-based:
Certainly! Here's the manual for editing the hosts file on Unix-based systems (including Linux and macOS):

**Unix-based (Linux and macOS):**

1. Open a terminal.
2. The hosts file is located at `/etc/hosts`. To edit this file, you need root privileges. Use the following command:

   ```bash
   sudo nano /etc/hosts
   ```

   You may be prompted to enter your password.

3. The nano text editor will open with the contents of the hosts file. Use the arrow keys to navigate to the end of the file.
4. Add your entries at the end of the file. For example:

   ```
   192.168.58.2    app.example.com
   192.168.58.2    app-v3.example.com
   ```
   Replace `192.168.58.2` with the actual IP address of your Minikube cluster if it's different.

5. To save the changes:
   - Press `Ctrl + X`
   - Press `Y` to confirm that you want to save the changes
   - Press `Enter` to confirm the file name

6. The file will be saved and nano will exit.

7. To ensure the changes take effect immediately, you can flush the DNS cache:
   - On macOS:
     ```bash
     sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
     ```
   - On Linux (varies by distribution, but this often works):
     ```bash
     sudo systemd-resolve --flush-caches
     ```

After making these changes, you should be able to access your Ingress-controlled services using the domain names you've specified.

Remember, modifying the hosts file affects your system's network behavior, so be careful and only add entries you're sure about. Also, these changes are local to your machine and won't affect other devices on your network.

Open your browser and play with different names of the applications, for example, try to open `app-v3.example.com/v3`, this should return an error, because there is no hosts that can service this request.

In case you deploy the configuration in cloud, for example AWS. Instead of having just IP address

```
PS H:\GitHub\k8s\14. Ingress in Kubernetes. Creating ingress on Minikube> kubectl get ing
NAME           CLASS   HOSTS                                ADDRESS          PORTS   AGE
main-ingress   nginx   app.example.com,app-v3.example.com   192.168.16.132   80      24m
```
you would have a DNS name of the LoadBalancer, and use allias records. For example, you we would have an actual domain name as `app.example.com` we would create a DNS record of our LoadBalancer to that domain name. As we mentioned previouslu, since the ingress works on Layer 7, it can inspect the request, see the `app.example.com` in the HEADER and send the packet to the correct host.



**NOTE!**
 In case the minikube cluster based on Docker fails to open the applications, disable the ingress addon service, run minikube tunnel in separated terminal and keep it running, return to the main termimal an enable the ingress addon service.
 In case the error still persists delete the whole cluster and try to build it with vmware driver and sufficiant resources. For example, as in this example, `minikube.exe start --cpus=4 --memory=8gb --disk-size=25gb --driver vmware`.