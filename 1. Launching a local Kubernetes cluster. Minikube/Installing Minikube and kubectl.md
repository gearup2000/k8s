## Install Minikube on Windows (Minikube cluster on VMware® Workstation 17 Pro)

* Download latest verson of minikube using PowerShell, run Powershell *as Administrator*

```
New-Item -Path 'c:\' -Name 'minikube' -ItemType Directory -Force
Invoke-WebRequest -OutFile 'c:\minikube\minikube.exe' -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing

```

* Add the `minikube.exe` binary to your `PATH`.

```
$oldPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)
if ($oldPath.Split(';') -inotcontains 'C:\minikube'){
  [Environment]::SetEnvironmentVariable('Path', $('{0};C:\minikube' -f $oldPath), [EnvironmentVariableTarget]::Machine)
}

```

* Start your cluster.

```
minikube start --driver vmware
```

To use vmware driver by default issue the command

```
minikube config set driver vmware
```

* Optional. You can change the default settings of VM to run your cluster by adding arguments like

```
minikube start --cpus=4 --memory=8gb --disk-size=25gb
```

The WMWare Workstation do not show the minikube VM on the list of VM machines. To make it visible Press **File** and choice **Scan for Virtual Machines...**. Check the folder **C:\Users\Your  Username\.minikube\machines\minikube**. Choice the VM file and press **Finish**. Now you should be able to see the running **minikube** VM on the list.

## Install kubectl on Windows

Please follow the instruction on [https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/](https://https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/).

Do not forget to add kubectl to the Environment Variables of your Windows. To do so, please follow the following steps.

Type env, on the Search, Choice **Edit the system Environment variables**, Press **Environment Variables**, on the **System variables** window select **Path** and press **Edit...** button, add the folder where you placed you kubectl.exe file. Press OK buttons to close the **Environment Variables** windows.

## Commands

***minikube command reference***


**addons**
Enable or disable a minikube addon

**cache**
Manage cache for images

**completion**
Generate command completion for a shell

**config**
Modify persistent configuration values

**cp**
Copy the specified file into minikube

**dashboard**
Access the Kubernetes dashboard running within the minikube cluster

**delete**
Deletes a local Kubernetes cluster

**docker-env**
Provides instructions to point your terminal’s docker-cli to the Docker Engine inside minikube. (Useful for building docker images directly inside minikube)

**help**
Help about any command

**image**
Manage images

**ip**
Retrieves the IP address of the specified node

**kubectl**
Run a kubectl binary matching the cluster version

**license**
Outputs the licenses of dependencies to a directory

**logs**
Returns logs to debug a local Kubernetes cluster

**mount**
Mounts the specified directory into minikube

**node**
Add, remove, or list additional nodes

**options**
Show a list of global command-line options (applies to all commands).

**pause**
pause Kubernetes

**podman-env**
Configure environment to use minikube’s Podman service

**profile**
Get or list the current profiles (clusters)

**service**
Returns a URL to connect to a service

**ssh**
Log into the minikube environment (for debugging)

**ssh-host**
Retrieve the ssh host key of the specified node

**ssh-key**
Retrieve the ssh identity key path of the specified node

**start**
Starts a local Kubernetes cluster

**status**
Gets the status of a local Kubernetes cluster

**stop**
Stops a running local Kubernetes cluster

**tunnel**
Connect to LoadBalancer services

**unpause**
unpause Kubernetes

**update-check**
Print current and latest version number

**update-context**
Update kubeconfig in case of an IP or port change

**version**
Print the version of minikube
