# Deployment in Kubernetes. Application Update Strategies

Kubernetes deployments manage the lifecycle of applications, including scaling, updating, and rolling back pods. Key strategies include Recreate, Rolling Update, Blue-Green, and Canary, each offering different methods for updating applications with minimal downtime.

The deployment is the highe level of resources in Kubernetes. In includeds the services, like: Replication Controllers, ReplicaSet and others. Deployments are responsible for creating, scaling, and updating the application's pods.

Deployment strategies provide a way to manage the deployment of applications in Kubernetes. They define the order in which the containers are deployed, the actions taken when a new version of the application is deployed, and the strategy for scaling the application. The primary deployment strategies in Kubernetes include:

1. **Rolling Update**: Updates the replicas one by one, ensuring that no pod is terminated during the update.
3. **Recreate**: Restarts all the replicas of the deployment.

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

Next, we use manifest `kubernetes-deployment.yaml` to define the deployment: `kubectl apply -f kubernetes-deployment.yaml`. The manifest file contains the same information as the previous commands, but in a more structured and easier to read format.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubernetes
  labels:
    app: kubernetes
spec:
  replicas: 5
  minReadySeconds: 10
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
    type: RollingUpdate
  selector:
    matchLabels:
      app: http-server
  template:
    metadata:
      labels:
        app: http-server
    spec:
      containers:
      - name: kubernetes-app
        image: kmi8000/kubernetes_multi:0.1
        ports:
        - containerPort: 8000
```

Open Lens, and check the amoune of pods in the `default` namespace. You should see 5 pods, all of which are running and ready. The names of the pods are constructed from the name of deployment, the index of ReplicaSet and the index of pod within the ReplicaSet as in the previous example.

For the next step let's create a new service `kubernetes-service.yaml` file, which will
define a Kubernetes Service of type `NodePort`. This type of service exposes the application on each Node's IP at a static port, allowing external traffic to access the application.

Here's a breakdown of the file:

```
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-service
spec:
  selector:
    app: http-server
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: NodePort
```

- `apiVersion: v1`: Specifies the API version.
- `kind: Service`: Indicates that this resource is a Service.
- `metadata`: Contains metadata about the Service, including its name (`kubernetes-service`).
- `spec`: Defines the desired state of the Service.
  - `selector`: Specifies the Pods targeted by this Service, identified by the label `app: http-server`.
  - `ports`: Defines the port configuration.
    - `protocol: TCP`: Specifies the protocol used.
    - `port: 80`: The port on which the Service is exposed.
    - `targetPort: 8000`: The port on the Pods to which traffic should be forwarded.
  - `type: NodePort`: Exposes the Service on each Node's IP at a static port, allowing external traffic to access the application.

This configuration ensures that the application is accessible externally via the Node's IP address and the specified port. If we open Lens, Network > Services, we can see that the Service `kubernetes-service` was successfully deployed and it is exposing the some NodePort. In my case it's 31557 port. To access the application, you can use the following URL: `http://<Node's IP>:<NodePort>`. Remember to replace `<Node's IP>` with the actual IP address of your Node. To get the Node's IP, you can use `kubectl get nodes -o wide`. If you are using a cloud provider, you can find the Node's IP in the cloud provider's console. In case of a local setup, you can use `minikube ip` to get the IP. Since in our case we are using Minikube, the command `minikube IP` is returning IP address as `192.168.16.132`. So, the URL would be `http://192.168.16.132:31557`. Open a web browser and paste the URL to access the application. You should see a simple "Hello world from hostname: <pod name>" message. For example, if you have a pod named `Hello world from hostname: kubernetes-6c85f7555c-bkt98`, the message would be "Hello world from hostname: kubernetes-6c85f7555c-bkt98". Since all 5 pods were registered to the Service, the traffic is evenly distributed across the pods. Each we refresh the page the message will change, providing hostnames of all 5 hosts. Please note that this is a very basic example and in a real-world scenario, you would need to consider more complex configurations, such as load balancing, autoscaling, and more.

# RollingUpdate

The RollingUpdate strategy allows you to update the application in a controlled manner, allowing you to minimize downtime and ensure a smooth transition. Here's an example of how you can use the RollingUpdate strategy in the Kubernetes deployment:

Our previous example used the RollingUpdate strategy with a maximum surge of 1 and a maximum unavailable of 1. This means that Kubernetes will try to maintain the desired number of replicas (5 in this case) during the update process. If the number of available replicas drops below the desired number, Kubernetes will stop new pods from being created and wait for the available replicas to recover. If the number of available replicas reaches the desired number, Kubernetes will start creating new pods to replace the old ones. This ensures that the application remains available during the update process. In our `kubernetes-deployment.yaml` file, we have can specified the RollingUpdate strategy like this:

```
spec:
  replicas: 5
  minReadySeconds: 10
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
    type: RollingUpdate
```

The replicas field specifies the desired number of replicas. The minReadySeconds field specifies the minimum number of seconds for which a newly created pod should be ready before it is considered available. The maxSurge and maxUnavailable fields specify the maximum number of pods that can be created during the update process and the maximum number of pods that can be unavailable during the update process, respectively. Please note that you should carefully consider the desired values for maxSurge and maxUnavailable based on your application's requirements and the expected traffic during the update process. If you set maxSurge to a high value, you may risk creating too many new pods during the update process, which could lead to resource exhaustion. If you set maxUnavailable to a high value, you may risk causing some pods to be unavailable during the update process, which could lead to downtime. In general, you should aim to set maxSurge and maxUnavailable to the same value to ensure a smooth transition. To test the RollingUpdate strategy, you can for example change the Docker image and apply the updated `kubernetes-deployment.yaml` file and observe the status of the pods during the update process. You can use `kubectl get pods -l app=http-server --watch` to watch the status of the pods and see if they are rolling out and rolling in smoothly.

Let's open 3 terminals to see the effect of the RollingUpdate strategy. Apply all commands in sequence, one by one. In the first terminal, apply command `kubectl get pods -l app=http-server --watch` to see the status of the pods. In the second terminal, apply command `kubectl apply -f kubernetes-deployment-updated-image.yaml` which is basically the same as `kubernetes-deployment.yaml` but changes the Docker image to `kmi8000/kubernetes_multi:0.2`. In third terminal, apply `kubectl rollout status deployment kubernetes` to see the status of the deployment. After the update process is complete, as can be observed in third terminal, press CTRL+C to exit the watch command in your first terminal.

The outputs should look something like this:

First terminal:

```
PS H:\GitHub\k8s\11. Deployment in Kubernetes. Application Update Strategies> kubectl get pods -l app=http-server --watch
NAME                          READY   STATUS    RESTARTS   AGE                                                           kubernetes-6c85f7555c-bkt98   1/1     Running   0          43s
kubernetes-6c85f7555c-qkqzp   1/1     Running   0          43s                                                           kubernetes-6c85f7555c-vcsks   1/1     Running   0          43s
kubernetes-6c85f7555c-x7cdc   1/1     Running   0          43s                                                           kubernetes-6c85f7555c-zxrcr   1/1     Running   0          43s
kubernetes-5df485c7f4-spd2l   0/1     Pending   0          0s                                                            kubernetes-5df485c7f4-spd2l   0/1     Pending   0          0s
kubernetes-6c85f7555c-vcsks   1/1     Terminating   0          55s                                                       kubernetes-5df485c7f4-spd2l   0/1     ContainerCreating   0          0s
kubernetes-5df485c7f4-ww7r6   0/1     Pending             0          0s                                                  kubernetes-5df485c7f4-ww7r6   0/1     Pending             0          0s
kubernetes-5df485c7f4-ww7r6   0/1     ContainerCreating   0          2s                                                  kubernetes-5df485c7f4-spd2l   1/1     Running             0          5s
kubernetes-5df485c7f4-ww7r6   1/1     Running             0          7s                                                  kubernetes-6c85f7555c-x7cdc   1/1     Terminating         0          71s
kubernetes-5df485c7f4-6m7qn   0/1     Pending             0          0s                                                  kubernetes-5df485c7f4-6m7qn   0/1     Pending             0          0s
kubernetes-5df485c7f4-6m7qn   0/1     ContainerCreating   0          0s                                                  kubernetes-5df485c7f4-6m7qn   1/1     Running             0          1s
kubernetes-6c85f7555c-qkqzp   1/1     Terminating         0          72s                                                 kubernetes-5df485c7f4-44ffv   0/1     Pending             0          0s
kubernetes-5df485c7f4-44ffv   0/1     Pending             0          0s                                                  kubernetes-5df485c7f4-44ffv   0/1     ContainerCreating   0          0s
kubernetes-5df485c7f4-44ffv   1/1     Running             0          2s                                                  kubernetes-6c85f7555c-vcsks   0/1     Error               0          86s
kubernetes-6c85f7555c-vcsks   0/1     Error               0          86s                                                 kubernetes-6c85f7555c-vcsks   0/1     Error               0          86s
kubernetes-6c85f7555c-zxrcr   1/1     Terminating         0          91s                                                 kubernetes-6c85f7555c-bkt98   1/1     Terminating         0          91s
kubernetes-5df485c7f4-xc8d6   0/1     Pending             0          0s                                                  kubernetes-5df485c7f4-xc8d6   0/1     Pending             0          0s
kubernetes-5df485c7f4-xc8d6   0/1     ContainerCreating   0          0s                                                  kubernetes-5df485c7f4-xc8d6   1/1     Running             0          1s
kubernetes-6c85f7555c-x7cdc   0/1     Error               0          101s                                                kubernetes-6c85f7555c-x7cdc   0/1     Error               0          101s
kubernetes-6c85f7555c-x7cdc   0/1     Error               0          101s                                                kubernetes-6c85f7555c-qkqzp   0/1     Error               0          102s
kubernetes-6c85f7555c-qkqzp   0/1     Error               0          102s                                                kubernetes-6c85f7555c-qkqzp   0/1     Error               0          102s
kubernetes-6c85f7555c-zxrcr   0/1     Error               0          2m1s                                                kubernetes-6c85f7555c-bkt98   0/1     Error               0          2m1s
kubernetes-6c85f7555c-bkt98   0/1     Error               0          2m1s                                                kubernetes-6c85f7555c-bkt98   0/1     Error               0          2m1s
kubernetes-6c85f7555c-zxrcr   0/1     Error               0          2m1s                                                kubernetes-6c85f7555c-zxrcr   0/1     Error               0          2m1s
```

The second terminal:

```
PS H:\GitHub\k8s\11. Deployment in Kubernetes. Application Update Strategies> kubectl apply -f .\kubernetes-deployment-updated-image.yaml
deployment.apps/kubernetes configured
```

The third terminal:

```
PS H:\GitHub\k8s\11. Deployment in Kubernetes. Application Update Strategies> kubectl rollout status deployment kubernetes Waiting for deployment "kubernetes" rollout to finish: 2 out of 5 new replicas have been updated...
Waiting for deployment "kubernetes" rollout to finish: 2 out of 5 new replicas have been updated...                        Waiting for deployment "kubernetes" rollout to finish: 2 out of 5 new replicas have been updated...
Waiting for deployment "kubernetes" rollout to finish: 2 out of 5 new replicas have been updated...                        Waiting for deployment "kubernetes" rollout to finish: 3 out of 5 new replicas have been updated...
Waiting for deployment "kubernetes" rollout to finish: 3 out of 5 new replicas have been updated...                        Waiting for deployment "kubernetes" rollout to finish: 3 out of 5 new replicas have been updated...
Waiting for deployment "kubernetes" rollout to finish: 4 out of 5 new replicas have been updated...                        Waiting for deployment "kubernetes" rollout to finish: 4 out of 5 new replicas have been updated...
Waiting for deployment "kubernetes" rollout to finish: 4 out of 5 new replicas have been updated...                        Waiting for deployment "kubernetes" rollout to finish: 4 out of 5 new replicas have been updated...
Waiting for deployment "kubernetes" rollout to finish: 4 of 5 updated replicas are available...                            Waiting for deployment "kubernetes" rollout to finish: 4 of 5 updated replicas are available...
deployment "kubernetes" successfully rolled out
```

If we look at the output of the first terminal, we can see that the pods are being updated with the new Docker image. The rollout status shows that the deployment has successfully updated all the replicas. The application should now be running the updated version. You can check the updated version by opening the address `http://192.168.16.132:31557` in the web browser. The new version should show the message as `Version 0.2 Hello world from hostname: kubernetes-5df485c7f4-44ffv`. This demonstrates a simple update strategy using Kubernetes rolling updates without any downtime.

Let's remove the deployment and see Recreate strategy in action.

Delete the deployment `kubectl delete deployments kubernetes`.

# Recreate Strategy

The Recreate strategy will cause Kubernetes to recreate all the pods for the deployment. The main difference between the Recreate and Rolling Update strategies is that Rolling Update will update the pods one by one, while Recreate will recreate all the pods at once, but only after the old pods are terminated.

Let's apply the deployment with the Recreate strategy:

`kubectl apply -f.\kubernetes-deployment-recreate-strategy.yaml --record`

The deployment will create a new deployment, but this time with Recreate strategy.

Check the Lens to see the pods being created.

To see the Recreate strategy in action, let's create a copy of `kubernetes-deployments-recreate.yaml` file, change the name as `kubernetes-deployments-recreate-updated-image.yaml` and change the Docker image to kubernetes_multi:0.2 in the part:

```
    spec:
      containers:
      - name: kubernetes-app
        image: kmi8000/kubernetes_multi:0.1
        ports:
        - containerPort: 8000
```

Let's open few terminal to see the Recreate strategy in action.

In first terminal we can apply the command as

```
while($true) {
    (New-Object System.Net.WebClient).DownloadString("http://{{your_server}}:31870/")
    Start-Sleep -Seconds 2
    Write-Host ""
}
```

which is PowerShell script to continuously fetch the updated version of the application. Replace `{{your_server}}` with your server IP address. And check the port that is esposed on Pods by kubernetes-service.

The same Linux (bash) alternative is:

```
while true; do curl http://{{your_server}}:31870/;sleep 2; echo; done
```

In the second terminal apply `kubectl get pods -l app=http-server --watch` command to see the pods being created and terminated.
In the third terminal apply `kubectl apply -f .\kubernetes-deployment-recreate-updated-image.yaml --record`. This will apply the updated deployment with Recreate strategy.
In the fourth terminal apply `kubectl rollout status deployment kubernetes`. It will show that the deployment is being updated with the new Docker image.

Let's checkt the outputs of terminals to see the Recreate strategy in action.

First terminal:

```
Hello world from hostname: kubernetes-6c85f7555c-g8sp9

Hello world from hostname: kubernetes-6c85f7555c-qdp58

Hello world from hostname: kubernetes-6c85f7555c-8w52b

Hello world from hostname: kubernetes-6c85f7555c-24ddf

Hello world from hostname: kubernetes-6c85f7555c-97rdx

Exception calling "DownloadString" with "1" argument(s): "Unable to connect to the remote server"
At line:2 char:5
+     (New-Object System.Net.WebClient).DownloadString("http://192.168. ...
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (:) [], MethodInvocationException
    + FullyQualifiedErrorId : WebException


Version 0.2
Hello world from hostname: kubernetes-5df485c7f4-6spgj

Version 0.2
Hello world from hostname: kubernetes-5df485c7f4-lkw9m

Version 0.2
Hello world from hostname: kubernetes-5df485c7f4-st7qj

Version 0.2
Hello world from hostname: kubernetes-5df485c7f4-9h6dd

Version 0.2
Hello world from hostname: kubernetes-5df485c7f4-st7qj
```

As can be seen, the Recreate strategy is working as expected. It removes the old pods and creates new ones with the new Docker image. At some point in time, it was a downtime as the output shows, and we got **unable to connect to the remote server** error.

The second terminal output shows the pods statuses, when old pods were terminated and new ones were created:

```
PS H:\GitHub\k8s\11. Deployment in Kubernetes. Application Update Strategies> kubectl get pods -l app=http-server --watch
NAME                          READY   STATUS    RESTARTS   AGE
kubernetes-6c85f7555c-24ddf   1/1     Running   0          30m
kubernetes-6c85f7555c-8w52b   1/1     Running   0          30m
kubernetes-6c85f7555c-97rdx   1/1     Running   0          30m
kubernetes-6c85f7555c-g8sp9   1/1     Running   0          30m
kubernetes-6c85f7555c-qdp58   1/1     Running   0          30m
kubernetes-6c85f7555c-97rdx   1/1     Terminating   0          33m
kubernetes-6c85f7555c-qdp58   1/1     Terminating   0          33m
kubernetes-6c85f7555c-8w52b   1/1     Terminating   0          33m
kubernetes-6c85f7555c-g8sp9   1/1     Terminating   0          33m
kubernetes-6c85f7555c-24ddf   1/1     Terminating   0          33m
kubernetes-6c85f7555c-97rdx   0/1     Error         0          34m
kubernetes-6c85f7555c-g8sp9   0/1     Error         0          34m
kubernetes-6c85f7555c-8w52b   0/1     Error         0          34m
kubernetes-6c85f7555c-qdp58   0/1     Error         0          34m
kubernetes-6c85f7555c-24ddf   0/1     Error         0          34m
kubernetes-5df485c7f4-st7qj   0/1     Pending       0          0s
kubernetes-5df485c7f4-st7qj   0/1     Pending       0          0s
kubernetes-5df485c7f4-6spgj   0/1     Pending       0          0s
kubernetes-5df485c7f4-4vbtq   0/1     Pending       0          0s
kubernetes-5df485c7f4-4vbtq   0/1     Pending       0          0s
kubernetes-5df485c7f4-6spgj   0/1     Pending       0          0s
kubernetes-5df485c7f4-9h6dd   0/1     Pending       0          0s
kubernetes-5df485c7f4-lkw9m   0/1     Pending       0          0s
kubernetes-5df485c7f4-9h6dd   0/1     Pending       0          0s
kubernetes-5df485c7f4-lkw9m   0/1     Pending       0          0s
kubernetes-5df485c7f4-st7qj   0/1     ContainerCreating   0          0s
kubernetes-5df485c7f4-6spgj   0/1     ContainerCreating   0          0s
kubernetes-5df485c7f4-lkw9m   0/1     ContainerCreating   0          0s
kubernetes-5df485c7f4-4vbtq   0/1     ContainerCreating   0          0s
kubernetes-5df485c7f4-9h6dd   0/1     ContainerCreating   0          0s
kubernetes-6c85f7555c-qdp58   0/1     Error               0          34m
kubernetes-6c85f7555c-qdp58   0/1     Error               0          34m
kubernetes-6c85f7555c-8w52b   0/1     Error               0          34m
kubernetes-6c85f7555c-8w52b   0/1     Error               0          34m
kubernetes-6c85f7555c-g8sp9   0/1     Error               0          34m
kubernetes-6c85f7555c-g8sp9   0/1     Error               0          34m
kubernetes-6c85f7555c-97rdx   0/1     Error               0          34m
kubernetes-6c85f7555c-97rdx   0/1     Error               0          34m
kubernetes-6c85f7555c-24ddf   0/1     Error               0          34m
kubernetes-6c85f7555c-24ddf   0/1     Error               0          34m
kubernetes-5df485c7f4-st7qj   1/1     Running             0          2s
kubernetes-5df485c7f4-6spgj   1/1     Running             0          2s
kubernetes-5df485c7f4-lkw9m   1/1     Running             0          2s
kubernetes-5df485c7f4-9h6dd   1/1     Running             0          3s
kubernetes-5df485c7f4-4vbtq   1/1     Running             0          3s
```

The third terminal output shows that the deployment has been configured AKA changed:

```
PS H:\GitHub\k8s\11. Deployment in Kubernetes. Application Update Strategies> kubectl apply -f .\kubernetes-deployments-recreate-updated-image.yaml --record
Flag --record has been deprecated, --record will be removed in the future
deployment.apps/kubernetes configured
```

The fourth terminal output shows the rollout status of the deployment:

```
PS H:\GitHub\k8s\11. Deployment in Kubernetes. Application Update Strategies> kubectl rollout status deployment kubernetes
Waiting for deployment "kubernetes" rollout to finish: 0 out of 5 new replicas have been updated...
Waiting for deployment "kubernetes" rollout to finish: 0 out of 5 new replicas have been updated...
Waiting for deployment "kubernetes" rollout to finish: 0 out of 5 new replicas have been updated...
Waiting for deployment "kubernetes" rollout to finish: 0 of 5 updated replicas are available...
Waiting for deployment "kubernetes" rollout to finish: 0 of 5 updated replicas are available...
Waiting for deployment "kubernetes" rollout to finish: 0 of 5 updated replicas are available...
Waiting for deployment "kubernetes" rollout to finish: 0 of 5 updated replicas are available...
Waiting for deployment "kubernetes" rollout to finish: 0 of 5 updated replicas are available...
Waiting for deployment "kubernetes" rollout to finish: 0 of 5 updated replicas are available...
deployment "kubernetes" successfully rolled out
```

This shows how the Recreate strategy works with the Kubernetes Deployment. When an update is required, the Deployment will remove the old pods and create new ones with the new Docker image.

# The --record flag and history of deployments

While testing the strateies, we used the `--record` flag to record the history of the deployments. The `--record` flag is a feature that records the actions taken by kubectl to modify resources. In this case, it recorded the actions taken to apply the kubernetes deployments.

We can see the history of the deployments using the `kubectl rollout history deployment kubernetes` command:

```
PS H:\GitHub\k8s\11. Deployment in Kubernetes. Application Update Strategies> kubectl rollout history deployment kubernetes
deployment.apps/kubernetes 
REVISION  CHANGE-CAUSE
1         kubectl.exe apply --filename=.\kubernetes-deployments-recreate.yaml --record=true
2         kubectl.exe apply --filename=.\kubernetes-deployments-recreate-updated-image.yaml --record=true
```

Let's add one more revision by applying commands manually, for example `kubectl set image deployment/kubernetes kubernetes-app=kmi8000/kubernetes_multi --record` and `kubectl set image deployment/kubernetes kubernetes-app=kmi8000/kubernetes_multi:0.1 --record`:

let's check the history again:

```
PS H:\GitHub\k8s\11. Deployment in Kubernetes. Application Update Strategies> kubectl rollout history deployment kubernetes
deployment.apps/kubernetes 
REVISION  CHANGE-CAUSE
2         kubectl.exe apply --filename=.\kubernetes-deployments-recreate-updated-image.yaml --record=true
3         kubectl.exe set image deployment/kubernetes kubernetes-app=kmi8000/kubernetes_multi --record=true
4         kubectl.exe set image deployment/kubernetes kubernetes-app=kmi8000/kubernetes_multi:0.1 --record=true
```

This shows that we have added two more revisions. The change-causes indicate the actions taken to update the deployments. This can backtrace the history of deployments, allowing us to identify the cause of an update and the specific changes made. Also to rollback to previous versions if needed. For example issuing `kubectl rollout undo deployment/kubernetes --to-revision=2` will revert the deployment to the revision 2 state.

if we apply `kubectl rollout undo deployment kubernetes` command, it will revert the deployment to the previous revision.

These revision history are holding by ReplicaSets, not directly by Deployments. That is why it is very important to keep old ReplicaSets and avoid of deleting them.
