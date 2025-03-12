# Overview

This Python code creates a simple HTTP server that responds with a message that includes the server's hostname. When you access this server via a web browser or HTTP client, it will return a response with the text "Hello world from hostname: <hostname>".

## Explanation

##### 1. Imports:

**Python**

```

from http.server import HTTPServer, BaseHTTPRequestHandler
import socket`
```

* HTTPServer and BaseHTTPRequestHandler are imported from the http.server module to create and handle HTTP server requests.
* socket is imported to get the hostname of the server.

##### 2. Custom Request Handler:

**Python**

```
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello world from hostname: ' + socket.gethostname().encode())`
```

SimpleHTTPRequestHandler is a subclass of BaseHTTPRequestHandler.

The do_GET method is overridden to handle GET requests. Here’s what happens inside this method:

`self.send_response(200)` - sends an HTTP 200 OK status code.

`self.end_headers()`     - ends the HTTP headers.

`self.wfile.write()`     - writes the response body to the client. It sends a message that says "Hello world from hostname: <hostname>", where <hostname> is the server's hostname obtained using socket.gethostname().

##### 3. Server Setup:

**Python**

```
SERVER_PORT = 8000
httpd = HTTPServer(('0.0.0.0', SERVER_PORT), SimpleHTTPRequestHandler)
print('Listening on port %s ...' % SERVER_PORT)
httpd.serve_forever()```


```

`SERVER_PORT = 8000`                                             - sets the port number to 8000.

`httpd = HTTPServer(('0.0.0.0', SERVER_PORT), SimpleHTTPRequestHandler)` - creates an instance of `HTTPServer` with the address `0.0.0.0` (which means it listens on all available interfaces) and the port 8000. It uses `SimpleHTTPRequestHandler` to handle incoming requests.

`print('Listening on port %s ...' % SERVER_PORT)`                     - prints a message indicating that the server is listening on port 8000.

`httpd.serve_forever()`                                           - starts the server and makes it listen for incoming HTTP requests indefinitely.

##### 5. Build Iamge:

**Docker**

Activate docker feature to build multi platform images.

`docker buildx create --use`

Build image.

`docker buildx build --platform linux/amd64,linux/arm64 -t kubernetes_multi . --output type=docker`

Add tag.

`docker tag kubernetes_multi:latest kmi8000/kubernetes_multi:0.1`

Push image

`docker push kmi8000/kubernetes_multi:0.1`

Create two more versions of the image named `kubernetes_multi:0.2` and `kubernetes-multi:0.3`. We will need them in the future. To do so uncomment the line `#self.wfile.write(b'Version 0.2\n')` by removing the `#` symbol, and build the `version 0.2` image. Repeat with `version 0.3`.

All done! Now the images are built to support multi platforms and avalable to download and use in **arm64** and **amd64** architectures.
