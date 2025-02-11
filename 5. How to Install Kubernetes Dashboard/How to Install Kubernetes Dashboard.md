# 5. How to Install Kubernetes Dashboard.

Dashboard is a web-based Kubernetes user interface. You can use Dashboard to deploy containerized applications to a Kubernetes cluster, troubleshoot your containerized application, and manage the cluster resources. You can use Dashboard to get an overview of applications running on your cluster, as well as for creating or modifying individual Kubernetes resources (such as Deployments, Jobs, DaemonSets, etc). For example, you can scale a Deployment, initiate a rolling update, restart a pod or deploy new applications using a deploy wizard.

Deploy a single cluster, take example of part 4. How to use kubectl with multiple kubernetes clusters.

### UPDATE

The minikube version v.1.35.0, has the options to activate a dashboard without installing any helm charts or any YAML files. To activate a dashboard run commands as...

`minikube.exe addons enable metrics-server` to enable metrics features and `minikube dashboard` to activate and run the Dashboard.

[Deploy and Access the Kubernetes Dashboard](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/)

Install helm in Windows by downloading the binary file and adding it to the Environment Variable of Windows.

Run the commands...

```
# Add kubernetes-dashboard repository
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
# Deploy a Helm Release named "kubernetes-dashboard" using the kubernetes-dashboard chart
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
```

Create a sample user to access the Dashboard by following instruction.

Create an yaml file with the name sa-dash.yaml. and add the following code..

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

Apply the file by `kubectl.exe apply -f .\sa-dash.yaml`

Run the `kubernetes-dashboard create token admin-user`
The output will show the token, copy it.

Run `kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443`.

The Dashboard will be available by https://localhost:8443. Open the link by your browser.

First login will ask the token, provide previosly copied token.

### The more detailed instruction can be found by following links...

[Deploy and Access the Kubernetes Dashboard](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/)
[Creating sample user](https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md)
