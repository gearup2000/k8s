15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes

Clean up and create new the cluster before starting.

Stop the cluster:
```bash
minikube stop
```

Delete the cluster:
```bash
minikube delete --all --purge
```

Start new cluster:
```bash
minikube.exe start --cpus=4 --memory=8gb --disk-size=25gb --driver vmware
```

Turn on the Dashboard in new terminal and keep it running:
```bash
minikube dashboard
```

Go back to the the first terminal and deploy a new deployment with NodePort(30001) as a service:

```bash
kubectl apply -f .\kubernetes-deploy.yaml
```

Check the IP and see if the service working properly:

```bash
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> minikube ip
192.168.16.132                                                                                                                                                   
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> curl http://192.168.16.132:30001

StatusCode        : 200
StatusDescription : OK
Content           : {72, 101, 108, 108...}
RawContent        : HTTP/1.0 200 OK
                    Date: Fri, 14 Mar 2025 02:35:43 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5

                    Hello world from hostname: kubernetes-default-dd99d9db6-87kxw
Headers           : {[Date, Fri, 14 Mar 2025 02:35:43 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 61

PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> 
```

If you get the the HTTP response **200** the service works as expected.

# Liveness Probes

## Liveness Probe with Command Execution

A Liveness probe in Kubernetes using command execution checks the health of a container by running a specified command inside the container. If the command returns a non-zero exit code, the probe fails, and Kubernetes restarts the container.

### How It Works

1. **Configuration**: You configure a Liveness probe in the container specification of your Pod. The probe runs a specified command inside the container.
2. **Periodic Checks**: Kubernetes periodically executes the command to determine the health of the container.
3. **Failure Handling**: If the command returns a non-zero exit code, Kubernetes considers the container unhealthy and restarts it.

### Example

The kubernetes-deploy-livenessProbe-exec.yaml file:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ubuntu
  labels:
    app: ubuntu
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ubuntu
  template:
    metadata:
      labels:
        app: ubuntu
    spec:
      containers:
      - name: ubuntu
        image: ubuntu
        args:
        - /bin/sh
        - -c
        - touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
          requests:
            memory: "64Mi"
            cpu: "250m"
        livenessProbe:
          exec:
            command:
            - cat
            - /tmp/healthy
          initialDelaySeconds: 5 # Defaults to 0 seconds. Minimum value is 0.
          periodSeconds: 5 # Default to 10 seconds. Minimum value is 1.
          timeoutSeconds: 1 # Defaults to 1 second. Minimum value is 1.
          successThreshold: 1 # Defaults to 1. Must be 1 for liveness and startup Probes. Minimum value is 1.
          failureThreshold: 3 # Defaults to 3. Minimum value is 1.
```

### Explanation

- **Command**: The Liveness probe runs the command `cat /tmp/healthy` inside the container.
- **Initial Delay**: The probe waits 5 seconds before performing the first check.
- **Period**: The probe performs the check every 5 seconds.
- **Timeout**: The probe times out if the command does not complete within 1 second.
- **Success Threshold**: The probe considers the container healthy if the command succeeds once.
- **Failure Threshold**: The probe considers the container unhealthy if the command fails 3 consecutive times.

The `args` section in the container specification defines the command and arguments that the container will run when it starts. In this case, the container runs a shell command (`/bin/sh -c`) with a series of commands separated by semicolons.

```yaml
args:
- /bin/sh
- -c
- touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600
```

- **`/bin/sh`**: This specifies the shell to use, which is `/bin/sh`.
- **`-c`**: This flag tells the shell to execute the following command string.
- **`touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600`**: This is the command string that the shell will execute.

**Breakdown of the Command String**

1. **`touch /tmp/healthy`**:
   - This command creates an empty file named `/tmp/healthy`. If the file already exists, it updates the file's timestamp.

2. **`sleep 30`**:
   - This command pauses the execution for 30 seconds.

3. **`rm -rf /tmp/healthy`**:
   - This command removes the `/tmp/healthy` file. The `-rf` flags ensure that the file is removed forcefully and recursively (if it were a directory).

4. **`sleep 600`**:
   - This command pauses the execution for 600 seconds (10 minutes).

**The purpose of the Command**

The purpose of this command sequence is to simulate a container that initially starts healthy but becomes unhealthy after 30 seconds:

- **Healthy State**: When the container starts, it creates the `/tmp/healthy` file, indicating that it is healthy.
- **Unhealthy State**: After 30 seconds, the container removes the `/tmp/healthy` file, indicating that it is no longer healthy.
- **Liveness Probe**: The liveness probe checks for the existence of the `/tmp/healthy` file. If the file is not found, the probe fails, and Kubernetes restarts the container.

This setup allows you to test the liveness probe's ability to detect and recover from an unhealthy state by restarting the container.

Apply the `kubectl apply -f kubernetes-deploy-livenessProbe-exec.yaml` configuration, and check the dashboard, to see how does work. You also could apply the command `kubectl get events --watch`.

Output of get events command:
```bash
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> kubectl get events --watch          
LAST SEEN   TYPE      REASON              OBJECT                         MESSAGE
2m50s       Normal    Scheduled           pod/ubuntu-6487f69dd8-7m5k7    Successfully assigned default/ubuntu-6487f69dd8-7m5k7 to minikube
12s         Normal    Pulling             pod/ubuntu-6487f69dd8-7m5k7    Pulling image "ubuntu"
2m41s       Normal    Pulled              pod/ubuntu-6487f69dd8-7m5k7    Successfully pulled image "ubuntu" in 7.651s (7.651s including waiting). Image size: 78130653 bytes.
11s         Normal    Created             pod/ubuntu-6487f69dd8-7m5k7    Created container: ubuntu
11s         Normal    Started             pod/ubuntu-6487f69dd8-7m5k7    Started container ubuntu
43s         Warning   Unhealthy           pod/ubuntu-6487f69dd8-7m5k7    Liveness probe failed: cat: /tmp/healthy: No such file or directory
43s         Normal    Killing             pod/ubuntu-6487f69dd8-7m5k7    Container ubuntu failed liveness probe, will be restarted
87s         Normal    Pulled              pod/ubuntu-6487f69dd8-7m5k7    Successfully pulled image "ubuntu" in 1.432s (1.432s including waiting). Image size: 78130653 bytes.
11s         Normal    Pulled              pod/ubuntu-6487f69dd8-7m5k7    Successfully pulled image "ubuntu" in 1.406s (1.406s including waiting). Image size: 78130653 bytes.
2m50s       Normal    SuccessfulCreate    replicaset/ubuntu-6487f69dd8   Created pod: ubuntu-6487f69dd8-7m5k7
2m50s       Normal    ScalingReplicaSet   deployment/ubuntu              Scaled up replica set ubuntu-6487f69dd8 from 0 to 1
0s          Warning   Unhealthy           pod/ubuntu-6487f69dd8-7m5k7    Liveness probe failed: cat: /tmp/healthy: No such file or directory
0s          Warning   Unhealthy           pod/ubuntu-6487f69dd8-7m5k7    Liveness probe failed: cat: /tmp/healthy: No such file or directory
0s          Warning   Unhealthy           pod/ubuntu-6487f69dd8-7m5k7    Liveness probe failed: cat: /tmp/healthy: No such file or directory
0s          Normal    Killing             pod/ubuntu-6487f69dd8-7m5k7    Container ubuntu failed liveness probe, will be restarted
0s          Normal    Pulling             pod/ubuntu-6487f69dd8-7m5k7    Pulling image "ubuntu"
0s          Normal    Pulled              pod/ubuntu-6487f69dd8-7m5k7    Successfully pulled image "ubuntu" in 1.403s (1.403s including waiting). Image size: 78130653 bytes.
0s          Normal    Created             pod/ubuntu-6487f69dd8-7m5k7    Created container: ubuntu
0s          Normal    Started             pod/ubuntu-6487f69dd8-7m5k7    Started container ubuntu
0s          Warning   Unhealthy           pod/ubuntu-6487f69dd8-7m5k7    Liveness probe failed: cat: /tmp/healthy: No such file or directory
1s          Warning   Unhealthy           pod/ubuntu-6487f69dd8-7m5k7    Liveness probe failed: cat: /tmp/healthy: No such file or directory
0s          Warning   Unhealthy           pod/ubuntu-6487f69dd8-7m5k7    Liveness probe failed: cat: /tmp/healthy: No such file or directory
1s          Normal    Killing             pod/ubuntu-6487f69dd8-7m5k7    Container ubuntu failed liveness probe, will be restarted
```
As can be seen from the output, each time the the `healthy` is removed, the probe restarts the container.

**Remove deployment by** `kubectl delete -f kubernetes-deploy-livenessProbe-exec.yaml`.



## Liveness Probe with TCP Socket

A Liveness probe in Kubernetes using a TCP socket checks the health of a container by attempting to establish a TCP connection to a specified port on the container. If the connection attempt fails, the probe fails, and Kubernetes restarts the container.

### How It Works

1. **Configuration**: You configure a Liveness probe in the container specification of your Pod. The probe attempts to establish a TCP connection to a specified port on the container.
2. **Periodic Checks**: Kubernetes periodically attempts to establish the TCP connection to determine the health of the container.
3. **Failure Handling**: If the connection attempt fails, Kubernetes considers the container unhealthy and restarts it.

### Example

Here is an example from the `kubernetes-deploy-livenessProbe-tcp.yaml` file:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubernetes-tcp
  labels:
    app: kubernetes
spec:
  replicas: 1
  selector:
    matchLabels:
      app: http-server-tcp
  template:
    metadata:
      labels:
        app: http-server-tcp
    spec:
      containers:
      - name: kubernetes-app
        image: kmi8000/kubernetes_multi:0.1
        ports:
        - containerPort: 8000
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
          requests:
            memory: "64Mi"
            cpu: "250m"
        livenessProbe:
          tcpSocket:
            port: 8000
          initialDelaySeconds: 15 # Defaults to 0 seconds. Minimum value is 0.
          periodSeconds: 10 # Default to 10 seconds. Minimum value is 1.
          timeoutSeconds: 1 # Defaults to 1 second. Minimum value is 1.
          successThreshold: 1 # Defaults to 1. Must be 1 for liveness and startup Probes. Minimum value is 1.
          failureThreshold: 3 # Defaults to 3. Minimum value is 1.
---
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-service-tcp
spec:
  selector:
    app: http-server-tcp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
      nodePort: 30002
  type: NodePort
```

### Explanation

- **tcpSocket**: The Liveness probe attempts to establish a TCP connection to port 8000 on the container.
- **initialDelaySeconds**: The probe waits 5 seconds before performing the first check.
- **periodSeconds**: The probe performs the check every 5 seconds.

If the TCP connection to port 8000 cannot be established, the probe fails, and Kubernetes restarts the container.

For example, if the we change the port from `8000` to `8001` in the following part;

```yaml
        livenessProbe:
          tcpSocket:
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
```
the Kubernetes will restart the container, there is no TCP services on port `8001`.

Let's apply the manifest file with port `8000` and check with curl:

```bash
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> curl http://192.168.16.132:30002


StatusCode        : 200
StatusDescription : OK
Content           : {72, 101, 108, 108...}
RawContent        : HTTP/1.0 200 OK
                    Date: Sat, 15 Mar 2025 01:17:28 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5

                    Hello world from hostname: kubernetes-tcp-685679b95b-q6gnv
Headers           : {[Date, Sat, 15 Mar 2025 01:17:28 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 58
```

let's now edit the `kubernetes-deploy-livenessProbe-tcp.yaml` file and change the port to `8001` and observe the events by `kubectl get events --watch` command.

```bash
0s          Warning   Unhealthy           pod/kubernetes-tcp-684d7b986c-zxq4n    Liveness probe failed: dial tcp 10.244.0.13:8001: connect: connection refused
0s          Warning   Unhealthy           pod/kubernetes-tcp-684d7b986c-zxq4n    Liveness probe failed: dial tcp 10.244.0.13:8001: connect: connection refused
0s          Warning   Unhealthy           pod/kubernetes-tcp-684d7b986c-zxq4n    Liveness probe failed: dial tcp 10.244.0.13:8001: connect: connection refused
0s          Normal    Killing             pod/kubernetes-tcp-684d7b986c-zxq4n    Container kubernetes-app failed liveness probe, will be restarted
0s          Normal    Pulled              pod/kubernetes-tcp-684d7b986c-zxq4n    Container image "kmi8000/kubernetes_multi:0.1" already present on machine
0s          Normal    Created             pod/kubernetes-tcp-684d7b986c-zxq4n    Created container: kubernetes-app
0s          Normal    Started             pod/kubernetes-tcp-684d7b986c-zxq4n    Started container kubernetes-app
0s          Warning   Unhealthy           pod/kubernetes-tcp-684d7b986c-zxq4n    Liveness probe failed: dial tcp 10.244.0.13:8001: connect: connection refused
0s          Warning   Unhealthy           pod/kubernetes-tcp-684d7b986c-zxq4n    Liveness probe failed: dial tcp 10.244.0.13:8001: connect: connection refused
0s          Warning   Unhealthy           pod/kubernetes-tcp-684d7b986c-zxq4n    Liveness probe failed: dial tcp 10.244.0.13:8001: connect: connection refused
0s          Normal    Killing             pod/kubernetes-tcp-684d7b986c-zxq4n    Container kubernetes-app failed liveness probe, will be restarted
```

The events command shows the status of the container, since the probe cannot establish the connection with port `8001`, the Kubernetes restarts the process of creating new pod, after 3 failures to connect to the container.


**Remove the deployment** `kubectl delete -f .\kubernetes-deploy-livenessProbe-tcp.yaml`.

### Summary

A TCP-based Liveness probe helps ensure that your application remains healthy by periodically checking the ability to establish a TCP connection to a specified port on the container. If the connection fails, Kubernetes restarts the container to recover from the unhealthy state.


## Liveness Probe with HTTP Request

A Liveness probe in Kubernetes using an HTTP request checks the health of a container by sending an HTTP GET request to a specified endpoint on the container. If the request fails or returns a non-2xx status code, the probe fails, and Kubernetes restarts the container.

### How It Works

1. **Configuration**: You configure a Liveness probe in the container specification of your Pod. The probe sends an HTTP GET request to a specified path and port on the container.
2. **Periodic Checks**: Kubernetes periodically sends the HTTP GET request to determine the health of the container.
3. **Failure Handling**: If the request fails or returns a non-2xx status code, Kubernetes considers the container unhealthy and restarts it.

### Example

Here is an example from the kubernetes-deploy-livenessProbe-http.yaml file:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubernetes-http
  labels:
    app: kubernetes
spec:
  replicas: 1
  selector:
    matchLabels:
      app: http-server-http
  template:
    metadata:
      labels:
        app: http-server-http
    spec:
      containers:
      - name: kubernetes-app
        image: kmi8000/kubernetes_multi:0.1.unhealthy
        ports:
        - containerPort: 8000
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
          requests:
            memory: "64Mi"
            cpu: "250m"
        livenessProbe:
          httpGet:
            path: /healthcheck
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-service-http
spec:
  selector:
    app: http-server-http
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
      nodePort: 30003
  type: NodePort
```

### Explanation

- **httpGet**: The Liveness probe sends an HTTP GET request to the `/healthcheck` path on port 8000 of the container.
- **initialDelaySeconds**: The probe waits 5 seconds before performing the first check.
- **periodSeconds**: The probe performs the check every 5 seconds.

If the `/healthcheck` endpoint does not return a successful response (2xx status code), the probe fails, and Kubernetes restarts the container.

### Summary

An HTTP-based Liveness probe helps ensure that your application remains healthy by periodically sending an HTTP GET request to a specified endpoint on the container. If the request fails or returns a non-2xx status code, Kubernetes restarts the container to recover from the unhealthy state.

Let's check it in practice:

```bash
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> kubectl apply -f .\kubernetes-deploy-livenessProbe-http.yaml
deployment.apps/kubernetes-http created
service/kubernetes-service-http created
```

In separated terminal run events watch `kubectl get events --watch` so we can observe what will happen. 

Now let's curl the /healthcheck endpoint, so after 5 request the container must fail, and Kubernetes will re-create the container.

```bash
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> curl http://192.168.16.132:30003/healthcheck


StatusCode        : 200
StatusDescription : OK
Content           : {83, 101, 114, 118...}
RawContent        : HTTP/1.0 200 OK
                    Custom-header-for-kubernetes-app: Awesome
                    Date: Sat, 15 Mar 2025 18:59:34 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5                                                                                                                                                                                                                                                                                                                                                                         Server is healthy, Status OK!                                                                                                                                                                                                                                                                                                                                                         
Headers           : {[Custom-header-for-kubernetes-app, Awesome], [Date, Sat, 15 Mar 2025 18:59:34 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 30



PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> curl http://192.168.16.132:30003/healthcheck


StatusCode        : 200
StatusDescription : OK
Content           : {83, 101, 114, 118...}
RawContent        : HTTP/1.0 200 OK
                    Custom-header-for-kubernetes-app: Awesome
                    Date: Sat, 15 Mar 2025 18:59:35 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5                                                                                                                                                                                                                                                                                                                                                                         Server is healthy, Status OK!                                                                                                                                                                                                                                                                                                                                                         
Headers           : {[Custom-header-for-kubernetes-app, Awesome], [Date, Sat, 15 Mar 2025 18:59:35 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 30



PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> curl http://192.168.16.132:30003/healthcheck


StatusCode        : 200
StatusDescription : OK
Content           : {83, 101, 114, 118...}
RawContent        : HTTP/1.0 200 OK
                    Custom-header-for-kubernetes-app: Awesome
                    Date: Sat, 15 Mar 2025 18:59:36 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5                                                                                                                                                                                                                                                                                                                                                                         Server is healthy, Status OK!                                                                                                                                                                                                                                                                                                                                                         
Headers           : {[Custom-header-for-kubernetes-app, Awesome], [Date, Sat, 15 Mar 2025 18:59:36 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 30



PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> curl http://192.168.16.132:30003/healthcheck


StatusCode        : 200
StatusDescription : OK
Content           : {83, 101, 114, 118...}
RawContent        : HTTP/1.0 200 OK
                    Custom-header-for-kubernetes-app: Awesome
                    Date: Sat, 15 Mar 2025 18:59:37 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5

                    Server is healthy, Status OK!

Headers           : {[Custom-header-for-kubernetes-app, Awesome], [Date, Sat, 15 Mar 2025 18:59:37 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 30



PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> curl http://192.168.16.132:30003/healthcheck


StatusCode        : 200
StatusDescription : OK
Content           : {83, 101, 114, 118...}
RawContent        : HTTP/1.0 200 OK
                    Custom-header-for-kubernetes-app: Awesome
                    Date: Sat, 15 Mar 2025 18:59:37 GMT
                    Server: BaseHTTP/0.6 Python/3.8.5

                    Server is healthy, Status OK!

Headers           : {[Custom-header-for-kubernetes-app, Awesome], [Date, Sat, 15 Mar 2025 18:59:37 GMT], [Server, BaseHTTP/0.6 Python/3.8.5]}
RawContentLength  : 30



PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> curl http://192.168.16.132:30003/healthcheck
curl : The remote server returned an error: (503) Server Unavailable.
At line:1 char:1
+ curl http://192.168.16.132:30003/healthcheck
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (System.Net.HttpWebRequest:HttpWebRequest) [Invoke-WebRequest], WebException
    + FullyQualifiedErrorId : WebCmdletWebResponseException,Microsoft.PowerShell.Commands.InvokeWebRequestCommand

PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes>
```

The events watch output:

```bash
0s          Normal    Created             pod/kubernetes-http-8cc8bb878-9w77v     Created container: kubernetes-app
0s          Normal    Started             pod/kubernetes-http-8cc8bb878-9w77v     Started container kubernetes-app
0s          Normal    Killing             pod/kubernetes-http-8cc8bb878-9w77v     Stopping container kubernetes-app
0s          Normal    ScalingReplicaSet   deployment/kubernetes-http              Scaled up replica set kubernetes-http-546f675b55 from 0 to 1
1s          Normal    SuccessfulCreate    replicaset/kubernetes-http-546f675b55   Created pod: kubernetes-http-546f675b55-wwlfq
0s          Normal    Scheduled           pod/kubernetes-http-546f675b55-wwlfq    Successfully assigned default/kubernetes-http-546f675b55-wwlfq to minikube
0s          Normal    Pulling             pod/kubernetes-http-546f675b55-wwlfq    Pulling image "kmi8000/kubernetes_multi_unhealthy:0.1.unhealthy"
0s          Normal    Pulled              pod/kubernetes-http-546f675b55-wwlfq    Successfully pulled image "kmi8000/kubernetes_multi_unhealthy:0.1.unhealthy" in 1.342s (1.342s including waiting). Image size: 881773133 bytes.
0s          Normal    Created             pod/kubernetes-http-546f675b55-wwlfq    Created container: kubernetes-app
0s          Normal    Started             pod/kubernetes-http-546f675b55-wwlfq    Started container kubernetes-app
0s          Warning   Unhealthy           pod/kubernetes-http-546f675b55-wwlfq    Liveness probe failed: HTTP probe failed with statuscode: 503
0s          Warning   Unhealthy           pod/kubernetes-http-546f675b55-wwlfq    Liveness probe failed: HTTP probe failed with statuscode: 503
0s          Warning   Unhealthy           pod/kubernetes-http-546f675b55-wwlfq    Liveness probe failed: HTTP probe failed with statuscode: 503
0s          Normal    Killing             pod/kubernetes-http-546f675b55-wwlfq    Container kubernetes-app failed liveness probe, will be restarted
```

From both outputs we can see that the deployment works as expected.

Remove deployment by `kubectl delete -f .\kubernetes-deploy-livenessProbe-http.yaml`.


## Readiness Probe with HTTP Request

A Readiness probe in Kubernetes using an HTTP request checks if a container is ready to start accepting traffic. If the probe fails, the container is marked as not ready, and it is removed from the service's endpoints, meaning it will not receive any traffic.

### How It Works

1. **Configuration**: You configure a Readiness probe in the container specification of your Pod. The probe sends an HTTP GET request to a specified path and port on the container.
2. **Periodic Checks**: Kubernetes periodically sends the HTTP GET request to determine if the container is ready to accept traffic.
3. **Failure Handling**: If the request fails or returns a non-2xx status code, Kubernetes considers the container not ready and removes it from the service's endpoints.

### Example

Here is an example from the [`15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes/kubernetes-deploy-readinessProbe-http.yaml`](15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in kubernetes-deploy-readinessProbe-http.yaml ) file:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubernetes-http-readinessprobe
  labels:
    app: kubernetes
spec:
  replicas: 1
  selector:
    matchLabels:
      app: http-server-default
  template:
    metadata:
      labels:
        app: http-server-default
    spec:
      containers:
      - name: kubernetes-app
        image: kmi8000/kubernetes_multi:0.1.unhealthy
        ports:
        - containerPort: 8000
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
          requests:
            memory: "64Mi"
            cpu: "250m"
        readinessProbe:
          httpGet:
            path: /healthcheck
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /healthcheck
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Explanation

- **readinessProbe**:
  - **httpGet**: The Readiness probe sends an HTTP GET request to the `/healthcheck` path on port 8000 of the container.
  - **initialDelaySeconds**: The probe waits 5 seconds before performing the first check.
  - **periodSeconds**: The probe performs the check every 5 seconds.

- **livenessProbe**:
  - **httpGet**: The Liveness probe also sends an HTTP GET request to the `/healthcheck` path on port 8000 of the container.
  - **initialDelaySeconds**: The probe waits 5 seconds before performing the first check.
  - **periodSeconds**: The probe performs the check every 5 seconds.

### Summary

- **Readiness Probe**: Ensures that the container is ready to accept traffic by periodically sending an HTTP GET request to the `/healthcheck` endpoint. If the probe fails, the container is marked as not ready and removed from the service's endpoints.
- **Liveness Probe**: Ensures that the container is running and healthy by periodically sending an HTTP GET request to the `/healthcheck` endpoint. If the probe fails, Kubernetes restarts the container.

This setup helps maintain the availability and reliability of your application by ensuring that only healthy and ready containers receive traffic. The main difference between Liveness and Readiness here us that the pod is not restarted, but just removed from the `http-server-default` service, in our case, from `http-server-default` service.


## Combined Liveness, Readiness, and Startup Probes

The kubernetes-deploy-all-Probes-http.yaml file defines a Kubernetes Deployment and Service with Liveness, Readiness, and Startup probes using HTTP requests and command execution. These probes ensure that the container is running, ready to accept traffic, and starts correctly. The Startup probe is usually implemented in case there is some legacy application, or any other application that needs more time to launch or initialize. In our example we will simulate the slow startup process of hipotetical application.

### How It Works

1. **Startup Probe**: Ensures that the container has started correctly by executing a command. If the probe fails, Kubernetes will not send traffic to the container.
2. **Readiness Probe**: Ensures that the container is ready to accept traffic by sending an HTTP GET request. If the probe fails, the container is marked as not ready and removed from the service's endpoints.
3. **Liveness Probe**: Ensures that the container is running and healthy by executing a command. If the probe fails, Kubernetes restarts the container.

### Example

Here is the content of the kubernetes-deploy-all-Probes-http.yaml file:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubernetes-http-allprobes
  labels:
    app: kubernetes
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kubernetes-http-allprobes
  template:
    metadata:
      labels:
        app: kubernetes-http-allprobes
    spec:
      containers:
      - name: kubernetes-app
        image: kmi8000/kubernetes_multi:0.1
        ports:
        - containerPort: 8000
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
          requests:
            memory: "64Mi"
            cpu: "250m"
        startupProbe:
          exec:
            command:
            - cat
            - /server-test.py
          initialDelaySeconds: 10
          failureThreshold: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          exec:
            command:
            - cat
            - /server-test.py
          failureThreshold: 1
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-http-allprobes-service
spec:
  selector:
    app: kubernetes-http-allprobes
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
      nodePort: 30004
  type: NodePort
```

### Explanation

1. **Startup Probe**:
   - **exec**: Executes the command `cat /server-test.py`.
   - **initialDelaySeconds**: Waits 10 seconds before performing the first check.
   - **failureThreshold**: Fails the probe if the command fails 30 consecutive times.
   - **periodSeconds**: Performs the check every 10 seconds.
   - **Explanation**: The Startup probe ensures that the container has started correctly by checking for the existence of the `/server-test.py` file. If the file is found, the probe succeeds. If the file is not found after 30 attempts, the probe fails, and the container is not marked as ready.

2. **Readiness Probe**:
   - **httpGet**: Sends an HTTP GET request to the `/` path on port 8000.
   - **initialDelaySeconds**: Waits 10 seconds before performing the first check.
   - **periodSeconds**: Performs the check every 5 seconds.
   - **Explanation**: The Readiness probe ensures that the container is ready to accept traffic by sending an HTTP GET request to the `/` endpoint. If the request fails or returns a non-2xx status code, the container is marked as not ready and removed from the service's endpoints.

3. **Liveness Probe**:
   - **exec**: Executes the command `cat /server-test.py`.
   - **failureThreshold**: Fails the probe if the command fails once.
   - **periodSeconds**: Performs the check every 10 seconds.
   - **Explanation**: The Liveness probe ensures that the container is running and healthy by checking for the existence of the `/server-test.py` file. If the file is not found, the probe fails, and Kubernetes restarts the container.

### Explanation

"When the Startup probe receives at least one successful response indicating the existence of the file `server-test.py`, which must be in the root folder, the Liveness probe will take over. The Liveness probe will then control the lifecycle of the pod and will restart the pod if the `/server-test.py` file is absent. The Readiness probe will send HTTP GET requests to port `8000` to check the availability of the pod."

### Summary

- **Startup Probe**: Ensures the container starts correctly by checking for the existence of the `/server-test.py` file.
- **Readiness Probe**: Ensures the container is ready to accept traffic by sending HTTP GET requests to the `/` endpoint on port 8000.
- **Liveness Probe**: Ensures the container remains healthy by checking for the existence of the `/server-test.py` file and restarting the container if the file is not found.

This setup helps maintain the availability and reliability of your application by ensuring that only healthy and ready containers receive traffic. The Startup probe ensures the container starts correctly, the Readiness probe ensures it is ready to accept traffic, and the Liveness probe ensures it remains healthy.

Let's deploy the manifest file and see how will it work.

```bash
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> kubectl apply -f .\kubernetes-deploy-all-Probes-http.yaml
deployment.apps/kubernetes-http-allprobes created
service/kubernetes-http-allprobes-service created
```

And check the events:

```bash
5b55-wwlfq_default(e141bb1d-f2dd-4995-a76d-0eb0a2de3e37)
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes>  kubectl get events --watch
LAST SEEN   TYPE      REASON              OBJECT                                            MESSAGE
18s         Normal    Scheduled           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Successfully assigned default/kubernetes-http-allprobes-5b8d5d7754-8gcfg to minikube
17s         Normal    Pulled              pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Container image "kmi8000/kubernetes_multi:0.1" already present on machine
17s         Normal    Created             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Created container: kubernetes-app
17s         Normal    Started             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Started container kubernetes-app
7s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory  
18s         Normal    SuccessfulCreate    replicaset/kubernetes-http-allprobes-5b8d5d7754   Created pod: kubernetes-http-allprobes-5b8d5d7754-8gcfg
18s         Normal    ScalingReplicaSet   deployment/kubernetes-http-allprobes              Scaled up replica set kubernetes-http-allprobes-5b8d5d7754 from 0 to 1 
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Normal    Killing             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Container kubernetes-app failed startup probe, will be restarted
```

Due the absent of the `/server-test` file, the probes proceeded successfully and restarted the pod.

Let's now login to the newly created pod and create `/server-test` file manually.

```bash
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> kubectl get pods
NAME                                         READY   STATUS    RESTARTS       AGE
kubernetes-default-dd99d9db6-87kxw           1/1     Running   2 (7h ago)     43h
kubernetes-http-allprobes-5b8d5d7754-8gcfg   0/1     Running   2 (107s ago)   13m
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> kubectl exec -it kubernetes-http-allprobes-5b8d5d7754-8gcfg -- bin/bash
root@kubernetes-http-allprobes-5b8d5d7754-8gcfg:/# touch /server-test.py
root@kubernetes-http-allprobes-5b8d5d7754-8gcfg:/# 
```

The output of events:

```bash
0s          Normal    Killing             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Container kubernetes-app failed startup probe, will be restarted
0s          Normal    Pulled              pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Container image "kmi8000/kubernetes_multi:0.1" already present on machine
0s          Normal    Created             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Created container: kubernetes-app
0s          Normal    Started             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Started container kubernetes-app
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Startup probe failed: cat: /server-test.py: No such file or directory
0s          Normal    Killing             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Container kubernetes-app failed startup probe, will be restarted
0s          Normal    Pulled              pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Container image "kmi8000/kubernetes_multi:0.1" already present on machine
0s          Normal    Created             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Created container: kubernetes-app
0s          Normal    Started             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Started container kubernetes-app
```

Running the `kubectl get pods` command shows the successful running pod:

```bash
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> kubectl get pods                                               
NAME                                         READY   STATUS    RESTARTS        AGE
kubernetes-default-dd99d9db6-87kxw           1/1     Running   2 (7h3m ago)    44h
kubernetes-http-allprobes-5b8d5d7754-8gcfg   1/1     Running   2 (5m31s ago)   16m
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> 
```

Let's now delete the `/server-test` file to see what will happen:

```bash
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> kubectl exec -it kubernetes-http-allprobes-5b8d5d7754-8gcfg -- bin/bash
root@kubernetes-http-allprobes-5b8d5d7754-8gcfg:/# rm -rf /server-test.py 
root@kubernetes-http-allprobes-5b8d5d7754-8gcfg:/# exit
exit
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> 
```

The events:

```bash
0s          Warning   Unhealthy           pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Liveness probe failed: cat: /server-test.py: No such file or directory
0s          Normal    Killing             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Container kubernetes-app failed liveness probe, will be restarted      
1s          Normal    Pulled              pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Container image "kmi8000/kubernetes_multi:0.1" already present on machine
0s          Normal    Created             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Created container: kubernetes-app
0s          Normal    Started             pod/kubernetes-http-allprobes-5b8d5d7754-8gcfg    Started container kubernetes-app
```

As can be seen, the liveness probe has restarted the container, since there is no `/server-test` file existing in the root folder.

The `kubectl get pods` command shows the ned ID of the pod, proving that the old pod was destroyed and new pod has been created.

Let's delete the deployment:

```bash
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> kubectl delete -f .\kubernetes-deploy-all-Probes-http.yaml     
deployment.apps "kubernetes-http-allprobes" deleted
service "kubernetes-http-allprobes-service" deleted
PS H:\GitHub\k8s\15. Probes-Liveness, Readiness, StartupProbe, http Headers, httpGet in Kubernetes> 
```