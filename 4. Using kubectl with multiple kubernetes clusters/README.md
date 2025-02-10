# Using kubectl with multiple kubernetes clusters.

Remove old clusters

```
minikube delete
```

Purge in case the minikube used any any other hypervisor

```
minikube delete --all --purge 
```

Start first kubernetes cluster with name k8s-cluster-1

```
minikube start --profile k8s-cluster-1
```

Start second kubernetes cluster with name k8s-cluster-2

```
minikube start --profile k8s-cluster-2
```

Check the config file which is located in ```C:\Users\<User Name>\.kube``` folder.

The output should show the the clusters configuration, and indicate the there is configurations of 2 clusters.

```
C:\Users\<User Name>\.kube> cat .\config
apiVersion: v1
clusters:
- cluster:
    certificate-authority: C:\Users\<User Name>\.minikube\ca.crt
    extensions:
    - extension:
        last-update: Sun, 09 Feb 2025 02:26:10 EET
        provider: minikube.sigs.k8s.io
        version: v1.25.2
      name: cluster_info
    server: https://192.168.16.133:8443
  name: k8s-cluster-1
- cluster:
    certificate-authority: C:\Users\<User Name>\.minikube\ca.crt
    extensions:
    - extension:
        last-update: Sun, 09 Feb 2025 03:04:22 EET
        provider: minikube.sigs.k8s.io
        version: v1.35.0
      name: cluster_info
    server: https://192.168.16.134:8443
  name: k8s-cluster-2
contexts:
- context:
    cluster: k8s-cluster-1
    extensions:
    - extension:
        last-update: Sun, 09 Feb 2025 02:26:10 EET
        provider: minikube.sigs.k8s.io
        version: v1.25.2
      name: context_info
    namespace: default
    user: k8s-cluster-1
  name: k8s-cluster-1
- context:
    cluster: k8s-cluster-2
    extensions:
    - extension:
        last-update: Sun, 09 Feb 2025 03:04:22 EET
        provider: minikube.sigs.k8s.io
        version: v1.35.0
      name: context_info
    namespace: default
    user: k8s-cluster-2
  name: k8s-cluster-2
current-context: k8s-cluster-2
kind: Config
preferences: {}
users:
- name: k8s-cluster-1
  user:
    client-certificate: C:\Users\<User Name>\.minikube\profiles\k8s-cluster-1\client.crt
    client-key: C:\Users\<User Name>\.minikube\profiles\k8s-cluster-1\client.key
- name: k8s-cluster-2
  user:
    client-certificate: C:\Users\<User Name>\.minikube\profiles\k8s-cluster-2\client.crt
    client-key: C:\Users\JOE-Admin\.minikube\profiles\k8s-cluster-2\client.key
```

The kubectl use config file and it might be exported from any other location, by **export KUBECONFIG=path_to_config_file**.

In case there is few config files, the might be added as a list by **export KUBECONFIG=path_tofirst__config_file:path_to_second_config_file**.

### Adding external cluster to the config file.

```

kubectl config set-cluster my-external-cluster --server=https://k8s.test.com:9443 --certificate-authority=path_to_the/ca_file
```

Checking the config file.

```
output ommited ...

- cluster: 
certificate-authority: path_to_the\ca_file
server: https://k8s.test.com:9443
name: my-external-cluster

output ommited ...

```

### Adding user to the config file.

```
kubectl config set-credentials temp --username=extra_user --password=superROOT

```

Checking the config file.

```
output ommited ...

- name: temp
user:
password: superROOT
username: extra_user  

output ommited ...
```

The credentials can be changed to use for example TOKEN.

```
kubectl config set-credentials temp --token=superTOKEN

```

```
output ommited ...

- name:     temp
user:
token: superTOKEN 

output ommited ...
```

After adding external cluster and extra_user to the config file, the context also must be added to the config file.

```
kubectl config set-context extra-context --cluster=my-external-cluster --user=temp --namespace=extra-namespace
```

Checking config file.

```
output ommited ...

contexts:
- context:
cluster: my-external-cluster
namespace: extra-namespace
user: temp
name: extra-context  

output ommited ...
```

## Interaction with multiple clusters

Appling commnand ```kubectl config current-context```

return the current-context ```k8s-cluster-2``` since it was initialized lasttly. Manually added entries do not change the order.

Appling commnand ```kubectl config get-contexts```

return the list of contexts

```

CURRENT     NAME            CLUSTER               AUTHINFO           NAMESPACE
            extra-context   my-external-cluster   temp               extra-namespace
            k8s-cluster-1   k8s-cluster-1         k8s-cluster-1      default
*           k8s-cluster-2   k8s-cluster-2         k8s-cluster-2      default

```

The asterix indicates the current-context.

If we apply the commnand ```kubectl get nodes```. The output will show the nodes of current cluster, which is k8s-cluster-2.

```
NAME            STATUS   ROLES           AGE     VERSION                                                                                                               k8s-cluster-2   Ready    control-plane   3h31m   v1.32.0 
```

Changing the context to use k8s-cluster-1.

```
C:\Users\Admin\.kube>kubectl config use-context k8s-cluster-1                                                                                                 
Switched to context "k8s-cluster-1".                                                                                                                                   C:\Users\Admin\.kube> kubectl get nodes                                                                                                                            NAME            STATUS   ROLES           AGE     VERSION                                                                                                               k8s-cluster-1   Ready    control-plane   3h38m   v1.32.0 
```

Checking the current context.

```
C:\Users\Admin\.kube> kubectl config get-contexts                                                                                                                
CURRENT     NAME            CLUSTER               AUTHINFO           NAMESPACE
            extra-context   my-external-cluster   temp               extra-namespace
*           k8s-cluster-1   k8s-cluster-1         k8s-cluster-1      default
            k8s-cluster-2   k8s-cluster-2         k8s-cluster-2      default

```

```
C:\Users\JOE-Admin\.kube> kubectl get nodes                                                                                                                            NAME            STATUS   ROLES           AGE     VERSION                                                                                                               k8s-cluster-1   Ready    control-plane   3h43m   v1.32.0   
```

Checking the clusters names and users.

```
C:\Users\Admin\.kube> kubectl config get-clusters                                                                                                                  NAME                                                                                                                                                                   k8s-cluster-1                                                                                                                                                          k8s-cluster-2                                                                                                                                                          my-external-cluster                                                                                                                                                  

C:\Users\Admin\.kube> kubectl config get-users                                                                                                                     NAME                                                                                                                                                                   k8s-cluster-1                                                                                                                                                          k8s-cluster-2                                                                                                                                                          temp               
```

### Removing external clusters and users from the config file.

```
kubectl config delete-context extra-context
                                                                                              
kubectl config delete-cluster my-external-cluster                                                                                          

kubectl config delete-user temp                                                                                                            

```

### Adding extra pod to the current cluster.

Checking what is the current context.

```
C:\Users\Admin\.kube> kubectl config get-contexts                                                                                                                
CURRENT     NAME            CLUSTER               AUTHINFO           NAMESPACE
            k8s-cluster-1   k8s-cluster-1         k8s-cluster-1      default
*           k8s-cluster-2   k8s-cluster-2         k8s-cluster-2      default

```

Checking the pods of all namespaces.

```

C:\Users\Admin\.kube> kubectl get pods --all-namespaces                                                                                                            NAMESPACE     NAME                                    READY   STATUS    RESTARTS        AGE                                                                            kube-system   coredns-668d6bf9bc-vzqw6                1/1     Running   0               3h54m                                                                          kube-system   etcd-k8s-cluster-2                      1/1     Running   0               3h54m                                                                          kube-system   kube-apiserver-k8s-cluster-2            1/1     Running   0               3h54m                                                                          kube-system   kube-controller-manager-k8s-cluster-2   1/1     Running   0               3h54m                                                                          kube-system   kube-proxy-t699w                        1/1     Running   0               3h54m                                                                          kube-system   kube-scheduler-k8s-cluster-2            1/1     Running   0               3h54m                                                                          kube-system   storage-provisioner                     1/1     Running   1 (3h54m ago)   3h54m 

```

Adding extra nginx pod from k8s.io to the current-context and checking the list of pods.

```
C:\Users\Admin\.kube> kubectl apply -f https://k8s.io/examples/pods/pod-nginx.yaml                                                                                 pod/nginx created                                                                                                                                                      C:\Users\Admin\.kube> kubectl get pods --all-namespaces                                                                                                            NAMESPACE     NAME                                    READY   STATUS    RESTARTS       AGE                                                                             default       nginx                                   0/1     Pending   0              90s                                                                             kube-system   coredns-668d6bf9bc-vzqw6                1/1     Running   0              4h1m                                                                            kube-system   etcd-k8s-cluster-2                      1/1     Running   0              4h1m                                                                            kube-system   kube-apiserver-k8s-cluster-2            1/1     Running   0              4h1m                                                                            kube-system   kube-controller-manager-k8s-cluster-2   1/1     Running   0              4h1m                                                                            kube-system   kube-proxy-t699w                        1/1     Running   0              4h1m                                                                            kube-system   kube-scheduler-k8s-cluster-2            1/1     Running   0              4h1m                                                                            kube-system   storage-provisioner                     1/1     Running   1 (4h1m ago)   4h1m  
```

Changing the context to the cluster k8s-cluster-1.

```
C:\Users\Admin\.kube> kubectl config use-context k8s-cluster-1                                                                                                     Switched to context "k8s-cluster-1".                                                                                                                                   C:\Users\Admin\.kube> kubectl get pods --all-namespaces                                                                                                            NAMESPACE     NAME                                    READY   STATUS    RESTARTS       AGE                                                                             kube-system   coredns-668d6bf9bc-q7hjn                1/1     Running   0              4h8m                                                                            kube-system   etcd-k8s-cluster-1                      1/1     Running   0              4h9m                                                                            kube-system   kube-apiserver-k8s-cluster-1            1/1     Running   0              4h9m                                                                            kube-system   kube-controller-manager-k8s-cluster-1   1/1     Running   0              4h9m                                                                            kube-system   kube-proxy-c9xpv                        1/1     Running   0              4h8m                                                                            kube-system   kube-scheduler-k8s-cluster-1            1/1     Running   0              4h9m                                                                            kube-system   storage-provisioner                     1/1     Running   1 (4h8m ago)   4h8m  
```

The nginx pod not listed here since it was installed on k8s-cluster-2 cluster.
