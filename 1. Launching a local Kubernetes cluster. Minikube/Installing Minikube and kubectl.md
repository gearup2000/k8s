## Install Minikube on Windows (Minikube cluster on VMware® Workstation 17 Pro)

Download latest verson of minikube using PowerShell, run Powershell *as Administrator*

```
New-Item -Path 'c:\' -Name 'minikube' -ItemType Directory -Force
Invoke-WebRequest -OutFile 'c:\minikube\minikube.exe' -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing

```

Add the `minikube.exe` binary to your `PATH`.

```
$oldPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)
if ($oldPath.Split(';') -inotcontains 'C:\minikube'){
  [Environment]::SetEnvironmentVariable('Path', $('{0};C:\minikube' -f $oldPath), [EnvironmentVariableTarget]::Machine)
}

```

Start your cluster

```
minikube start --driver vmware
```

Optional. You can change the default settings of VM to run your cluster by adding arguments like

```
minikube start --cpus=4 --memory=8gb --disk-size=25gb
```

The WMWare Workstation do not show the minikube VM on the list of VM machines. To make it visible Press **File** and choice **Scan for Virtual Machines...**. Check the folder **C:\Users\Your  Username\.minikube\machines\minikube**. Choice the VM file and press **Finish**. Now you should be able to see the running **minikube **VM on the list.
