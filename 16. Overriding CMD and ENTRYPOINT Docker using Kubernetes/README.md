# Overriding CMD and ENTRYPOINT Docker using Kubernetes.

## Basics of ENTRYPOINT and CMD.

The `CMD` and `ENTRYPOINT` instructions in a Dockerfile both specify what command should be run when a container starts, but they serve slightly different purposes and have different behaviors.

### CMD

- **Purpose**: The `CMD` instruction provides default arguments for the `ENTRYPOINT` instruction. If `ENTRYPOINT` is not specified, `CMD` sets the command to be executed.
- **Overriding**: The command specified in `CMD` can be overridden at runtime by providing additional arguments to `docker run`.
- **Usage**: It is often used to provide default behavior that can be overridden if needed.

### ENTRYPOINT

- **Purpose**: The `ENTRYPOINT` instruction sets the command and arguments that will be executed when the container starts. It is intended to be the main command that always runs.
- **Overriding**: The command specified in `ENTRYPOINT` cannot be overridden at runtime with `docker run` unless the `--entrypoint` flag is used.
- **Usage**: It is often used to ensure that a specific command is always run, regardless of any additional arguments provided.

### Example

Here is an example Dockerfile that uses both `CMD` and `ENTRYPOINT`:

```dockerfile
FROM ubuntu:latest

# Set the entry point to a script
ENTRYPOINT ["/usr/bin/my_script.sh"]

# Provide default arguments for the entry point
CMD ["arg1", "arg2"]
```

In this example:

- The `ENTRYPOINT` instruction sets `/usr/bin/my_script.sh` as the command to be executed when the container starts.
- The `CMD` instruction provides default arguments `arg1` and `arg2` for the entry point.

### Overriding Behavior

- **Default Behavior**: When you run the container without additional arguments, it will execute `/usr/bin/my_script.sh arg1 arg2`.
- **Overriding CMD**: You can override the `CMD` arguments by providing additional arguments to `docker run`:
  ```sh
  docker run my_image arg3 arg4
  ```
  This will execute `/usr/bin/my_script.sh arg3 arg4`.
- **Overriding ENTRYPOINT**: To override the `ENTRYPOINT`, you need to use the `--entrypoint` flag:
  ```sh
  docker run --entrypoint /bin/bash my_image
  ```
  This will start a Bash shell instead of running `/usr/bin/my_script.sh`.

### Summary

- **CMD**: Provides default arguments for the entry point or sets the command to be executed if `ENTRYPOINT` is not specified. It can be easily overridden at runtime.
- **ENTRYPOINT**: Sets the main command to be executed when the container starts. It is intended to be the primary command and is not easily overridden without using the `--entrypoint` flag.

Understanding the difference between `CMD` and `ENTRYPOINT` allows you to design more flexible and robust Docker images that can be customized at runtime.

There is two different methods declaring the `ENTRYPOINT` and `CMD`.

Let's take a look at the Dockerfiles from `Docker-entrypoint-exec` and `Docker-entrypoint-shell` folders.

Dockerfile of Docker-entrypoint-exec:
```Dockerfile
FROM python:3.8.5
COPY server.py /server.py
ENTRYPOINT ["python3","-u", "server.py"]
```

Dockerfile of Docker-entrypoint-shell:
```Dockerfile
FROM python:3.8.5
COPY server.py /server.py
ENTRYPOINT python3 -u server.py
```

The form `ENTRYPOINT ["python3","-u", "server.py"]` ensures that the command is executed directly without invoking a shell. It is more predictable and avoids potential issues with shell interpretation. To override this `ENTRYPOINT`, you need to use the `--entrypoint` flag with `docker run`.

While the form `ENTRYPOINT python3 -u server.py` invokes a shell to run the command. It allows for shell features like variable substitution, but it can be less predictable and may introduce issues with escaping characters. To override this `ENTRYPOINT`, you can provide a new command directly with `docker run`.

The same is applicable to `CMD` command.

Let's build the images and see the difference between.

```bash
 docker buildx build --platform linux/amd64,linux/arm64 -t kubernetes_multi_entrypoint_exec . --output type=docker
```

```bash
 docker buildx build --platform linux/amd64,linux/arm64 -t kubernetes_multi_entrypoint_shell . --output type=docker
```

Check the images:

```bash
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes\Docker-entrypoint-exec> docker images
REPOSITORY                          TAG               IMAGE ID       CREATED          SIZE
kubernetes_multi_entrypoint_exec    latest            e40472d63992   27 minutes ago   1.62GB
kubernetes_multi_entrypoint_shell   latest            f5ff2eae43fe   27 minutes ago   1.62GB
moby/buildkit                       buildx-stable-1   c5137fdd7737   11 days ago      306MB
```
Run Docker images:

```bash
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes> docker run -d -p 11111:8000 kubernetes_multi_entrypoint_exec
4861fcd6721dc66da7257a50772fcc508ccc8128aa7337e18acb87a22fa75d12
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes> docker run -d -p 22222:8000 kubernetes_multi_entrypoint_shell
a31a6d47b14c6f6701cff8181a412118cb2829d6242ac784aa51f4cc6375e005
```

Check if the images are running:

```bash
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes> docker ps
CONTAINER ID   IMAGE                               COMMAND                  CREATED          STATUS          PORTS                     NAMES
a31a6d47b14c   kubernetes_multi_entrypoint_shell   "/bin/sh -c 'python3…"   14 seconds ago   Up 14 seconds   0.0.0.0:22222->8000/tcp   eloquent_beaver
4861fcd6721d   kubernetes_multi_entrypoint_exec    "python3 -u server.py"   43 seconds ago   Up 42 seconds   0.0.0.0:11111->8000/tcp   festive_agnesi
a502fc8f434e   moby/buildkit:buildx-stable-1       "buildkitd --allow-i…"   44 minutes ago   Up 44 minutes                             buildx_buildkit_zealous_dhawan0
```

Login to each container in separated terminals so we can compare the differences:

First terminal (exec):

```bash
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes> docker exec -it 4861fcd6721d sh
# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.1  0.1  24928 17456 ?        Ss   00:54   0:00 python3 -u server.py
root           7  0.0  0.0   2392   692 pts/0    Ss   00:59   0:00 sh
root          13  0.0  0.0   9396  3012 pts/0    R+   01:00   0:00 ps aux
```

Second terminal (shell):

```bash
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes> docker exec -it a31a6d47b14c sh
# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   2392   752 ?        Ss   00:55   0:00 /bin/sh -c python3 -u server.py
root           7  0.0  0.1  24936 17752 ?        S    00:55   0:00 python3 -u server.py
root           8  0.0  0.0   2392   744 pts/0    Ss   00:59   0:00 sh
root          14  0.0  0.0   9396  3000 pts/0    R+   01:00   0:00 ps aux
```

The outputs of `ps aux` command (which shows all running processes), already shows, that in exec-container the script `server.py`executed directly without invoking a shell. While in shell-container execution go through the shell process, which then run the child process `python3 -u server.py`.
Obviously the shell process `/bin/sh-c python3 -u server.py` is unnecessary and redundant.

Also, in case of issuing commands like `SIGTERM` which is a signal used to request a process to terminate gracefully, which can be sent by other processes or the system itself, or `SIGKILL` which is a signal used to forcefully terminate a process without allowing it to perform any cleanup operations., the shell process `/bin/sh` will not send them to the child process `python3 -u server.py`.

Oppositly, in case of **exec** method, these kind of signals can be sent to the `python3 -u server.py` application.

Beside that, to use **shell** method the image **MUST** include the shell binary file, for example `bash`. Otherwise, the shell script will not be executed and that would cause that image to crash.

Let's stop our docker containers `docker stop 4861fcd6721d`, `docker stop a31a6d47b14c` and move forward.

## Overriding CMD and ENTRYPOINT Docker using Kubernetes.

To see the overriding in practice check the folder the folder **Docker** of 16. Overriding CMD and ENTRYPOINT Docker using Kubernetes part.

The folder contains few files like Python scripts that inlucdes the `server.py` and `server-default.py` scripts and the  `Dockerfile`. The `server.py` is a simple HTTP server that dynamically generates an HTML response based on command-line arguments. It prints the hostname, interval, desired count, and a custom string argument, followed by a looped output of the current time.

Example usage:

   Run the script with three command-line arguments:
   ```bash
   python3 server.py <interval> <desired_count> <string_arg>
   ```
   Example:
   ```bash
   python3 server.py 2 5 "Hello World"
   ```

2. **Access the Server**:
   Open a web browser to access the server by the following link `http://localhost:8000`

3. **Response**:
   The server responds with an HTML page containing:
   - The hostname of the server.
   - The interval, desired count, and custom string argument.
   - A looped output of the current time for the specified number of iterations.
Example responce:
```html
Hello from hostname: DESKTOP-427DTG3

Interval: 2

Desired count of print: 5

Text arg: Hello World

1. Current time: 01:47:55
2. Current time: 01:47:57
3. Current time: 01:47:59
4. Current time: 01:48:01
5. Current time: 01:48:03

End of loop.
```

The `server-default.py` file accepts the only one argument. The purpose of this script is to show that Kubernetes is able to overide the **ENTRYPOINT** as well.

The Dockerfile contains the following commands:

```Dockerfile
FROM python:3.8.5
COPY server.py /server.py
COPY server-default.py /server-default.py
ENTRYPOINT ["python3","-u", "server.py"]
CMD ["1","5","Hello World"]
```

This Dockerfile creates a flexible Docker image that runs `server.py` by default with arguments specified in `CMD`. It also includes `server-default.py` to demonstrate how the `ENTRYPOINT` or `CMD` can be overridden. The default behavior is to run `server.py` with an interval of `1` second, `5` iterations, and the string `"Hello World"`. However, both the script and its arguments can be customized at runtime, making the image highly versatile.

To summarize all together:

1. **Dockerfile**:
   - **`ENTRYPOINT`**: Runs `server.py` by default (`python3 -u server.py`).
   - **`CMD`**: Provides default arguments (`1`, `5`, `"Hello World"`) for `server.py`.

2. **`server.py`**:
   - A Python HTTP server that dynamically generates an HTML response based on command-line arguments (`interval`, `desired_count`, `string_arg`).
   - Outputs the hostname, interval, desired count, and a looped current time.

3. **`server-default.py`**:
   - A simpler HTTP server that accepts only one argument (`string_arg`).
   - Demonstrates how Kubernetes can override the `ENTRYPOINT`.

4. **Overriding Behavior**:
   - **CMD**: Can be overridden by passing arguments during `docker run`.
   - **ENTRYPOINT**: Can be overridden using the `--entrypoint` flag.

5. **Key Observations**:
   - Using `ENTRYPOINT` in **exec form** (`["python3", "-u", "server.py"]`) avoids unnecessary shell processes and ensures signals like `SIGTERM` are sent directly to the application.
   - Using **shell form** (`python3 -u server.py`) introduces a shell process (`/bin/sh`), which can be redundant and may not forward signals to the child process.

6. **Kubernetes**:
   - Demonstrates how Kubernetes can override `ENTRYPOINT` and `CMD` to run alternative scripts like `server-default.py`.

Let's creata a new image and proceed with the practice part.

Creating a new image:
```PS
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes\Docker> docker buildx build --platform linux/amd64,linux/arm64 -t kmi8000/kubernetes_multi_ep_cmd:1.0.args . --output type=docker
```

Running the image locally:

```PS
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes\Docker> docker run -d -p 8000:8000 kmi8000/kubernetes_multi_ep_cmd:1.0.args
54e4367bd262a8ad1b95c42c7f80019c8d0a8b94b6ad7d6b8bb3b16ec273cc0a
```

Open the http://localhost:8000 and see that the provided default arguments are used as intended. The hosname must be container name.

```html
Hello from hostname: 54e4367bd262

Interval: 1

Desired count of print: 5

Text arg: Hello World

1. Current time: 00:48:04
2. Current time: 00:48:05
3. Current time: 00:48:06
4. Current time: 00:48:07
5. Current time: 00:48:08

End of loop.
```

Let's now stop the container and change the default `CMD` arguments by providing them via command-line.

Stop the container:

```PS
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes\Docker> docker ps
CONTAINER ID   IMAGE                                      COMMAND                  CREATED         STATUS         PORTS                    NAMES
54e4367bd262   kmi8000/kubernetes_multi_ep_cmd:1.0.args   "python3 -u server.p…"   2 minutes ago   Up 2 minutes   0.0.0.0:8000->8000/tcp   serene_carver
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes\Docker> docker stop 54e4367bd262
54e4367bd262
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes\Docker> docker ps
CONTAINER ID   IMAGE                           COMMAND                  CREATED      STATUS          PORTS     NAMES
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes\Docker> 
```

Oeverriding the default `CMD` arguments:

```PS
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes\Docker> docker run -d -p 8000:8000 kmi8000/kubernetes_multi_ep_cmd:1.0.args 2 3 "I changed CMD arguments"
e48da56645ab57459c20210ebf3c64ea91ee378b0d2c5bcfff5e0573d51d97e7
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes\Docker> 
```

Open the http://localhost:8000/ by web browser and see the results:

```html
Hello from hostname: e48da56645ab

Interval: 2

Desired count of print: 3

Text arg: I changed CMD arguments

1. Current time: 00:54:33
2. Current time: 00:54:35
3. Current time: 00:54:37

End of loop.
```

As can be seen, we have successfully changed the CMD arguments, by chaning the interval, amount of messages and the Text argument.

Tests went successfully. Now, let's stop it again and push it to the DockerHub, so we can create a Kubernetes cluster out of this image.

```PS
PS H:\GitHub\k8s\16. Overriding CMD and ENTRYPOINT Docker using Kubernetes\Docker> docker push kmi8000/kubernetes_multi_ep_cmd:1.0.args
The push refers to repository [docker.io/kmi8000/kubernetes_multi_ep_cmd]
8ad241e996e9: Pushed
ad7c41999aa9: Pushed
a4850b8bdbb7: Pushed
71e126169501: Pushed
4b1202c4ddac: Pushed
bafa488e12a8: Pushed
1af28a55c3f3: Pushed
f110d64c2021: Pushed
aeac7ec27be8: Pushed
0994bd0592ba: Pushed
416533994968: Pushed
7b0157cfd609: Pushed
57df1a1f1ad8: Pushed
03f1c9932170: Pushed
d780a22c13bc: Pushed
65b3db15f518: Pushed
d3a32671b631: Pushed
1b580f9ce4ce: Pushed
12d85bccbc95: Pushed
3e3b8947ed83: Pushed
ff11255613a7: Pushed
ce90b30fd090: Pushed
1.0.args: digest: sha256:e1dc582deac3c91aa5288cfcb376b86e64a18b4cbdeecfb169a6c8eaf409b131 size: 1609
```
Create a new cluster `minikube start` and change the working folder to the 16. Overriding CMD and ENTRYPOINT Docker using Kubernetes.
Run deployment:


