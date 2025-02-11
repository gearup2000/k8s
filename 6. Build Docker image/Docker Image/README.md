# Creating Dockerfile, building, puhsing and removing images.

Download Dockerfile, index.php and custom.conf from the repository

To be able create multi platform images, the feature must be activated by `docker buildx create --use`.

After that run

`docker buildx build --platform linux/amd64,linux/arm64 -t k8sphp_multi . --output type=docker`.

Create a repository in DockerHub website and rename your local docker image:

`docker tag k8sphp_multi:latest Your_nickname/Repository_name:latest`.

My example `docker tag k8sphp_multi:latest kmi8000/k8sphp_multi:latest`.

Push the Docker Image to DockerHub:

My example `docker push kmi8000/k8sphp_multi:latest`

Check the list of images.

```
H:\Docker Image> docker images                          
REPOSITORY             TAG               IMAGE ID       CREATED          SIZE
kmi8000/k8sphp_multi   latest            2316c07bc6c3   3 hours ago      648MB                                                                                          k8sphp_multi           latest            2316c07bc6c3   3 hours ago      648MB
moby/buildkit          buildx-stable-1   14aa1b4dd92e   3 weeks ago      306MB
kmi8000/k8sphp         latest            a1721362d4ef   16 months ago    466MB                                                                                          k8sphpamd64            0.1               2af50161f8bf   16 months ago    466MB                                                                                          ```
```

Remove any unnecessary images, for example **k8sphpamd64:0.1**.

`docker rmi k8sphpamd64:0.1`

Login to the DockerHub. Provide credentials if needed.

```
H:\Docker Image> docker login

Authenticating with existing credentials...
Login Succeeded
```

Push image to the DockerHub.

`docker push kmi8000/k8sphp_multi:latest`
