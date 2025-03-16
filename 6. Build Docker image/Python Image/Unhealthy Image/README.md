# Overview

## Docker image that simulates failure of the web server.

The content of the server.py file:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthcheck':
            if count <= 5:
                self.send_response(200)
                self.send_header("Custom-header-for-kubernetes-app", "Awesome")
                self.end_headers()
                self.wfile.write(b'Server is healthy, Status OK!\n')
            else:
                self.send_response(503)
                self.end_headers()
                self.wfile.write(b'Server is unhealthy, Status Service Unavailable!\n')
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello world from hostname: ' + socket.gethostname().encode())

count = 1
SERVER_PORT = 8000
httpd = HTTPServer(('0.0.0.0', SERVER_PORT), SimpleHTTPRequestHandler)
print('Listening on port %s ...' % SERVER_PORT)
while 'true':
    httpd.handle_request()
    count += 1
```

### Explanation

1. **Imports**:
   - `HTTPServer` and `BaseHTTPRequestHandler` are imported from the `http.server` module to create and handle HTTP server requests.
   - `socket` is imported to get the hostname of the server.

2. **Custom Request Handler**:
   - `SimpleHTTPRequestHandler` is a subclass of `BaseHTTPRequestHandler`.
   - The `do_GET` method is overridden to handle GET requests. Inside this method:
     - **Health Check Endpoint**:
       - If the request path is `/healthcheck`, the server responds based on the value of `count`.
       - If `count` is less than or equal to 5:
         - Sends an HTTP 200 OK status code.
         - Adds a custom header `Custom-header-for-kubernetes-app` with the value `Awesome`.
         - Ends the HTTP headers.
         - Writes the response body `Server is healthy, Status OK!`.
       - If `count` is greater than 5:
         - Sends an HTTP 503 Service Unavailable status code.
         - Ends the HTTP headers.
         - Writes the response body `Server is unhealthy, Status Service Unavailable!`.
     - **Default Response**:
       - For any other request path, the server responds with:
         - An HTTP 200 OK status code.
         - Ends the HTTP headers.
         - Writes the response body `Hello world from hostname: <hostname>`, where `<hostname>` is the server's hostname obtained using `socket.gethostname()`.

3. **Server Setup**:
   - `count = 1`: Initializes the `count` variable to 1.
   - `SERVER_PORT = 8000`: Sets the port number to 8000.
   - `httpd = HTTPServer(('0.0.0.0', SERVER_PORT), SimpleHTTPRequestHandler)`: Creates an instance of `HTTPServer` with the address `0.0.0.0` (which means it listens on all available interfaces) and the port 8000. It uses `SimpleHTTPRequestHandler` to handle incoming requests.
   - `print('Listening on port %s ...' % SERVER_PORT)`: Prints a message indicating that the server is listening on port 8000.
   - `while 'true':`: Starts an infinite loop to handle incoming requests.
     - `httpd.handle_request()`: Handles a single HTTP request.
     - `count += 1`: Increments the `count` variable by 1 after each request.

### Summary

The server.py file creates a simple HTTP server that listens on port 8000. It has two main functionalities:
- **Health Check Endpoint**: When accessed via the `/healthcheck` path, it responds with a status based on the number of requests handled. For the first 5 requests, it responds with a 200 OK status and a custom header. After that, it responds with a 503 Service Unavailable status.
- **Default Response**: For any other request path, it responds with a message that includes the server's hostname.

The server runs indefinitely, handling GET requests and updating the `count` variable to simulate a change in health status over time.

##### 5. Build Iamge:

**Docker**

Activate docker feature to build multi platform images.

`docker buildx create --use`

Build image.

`docker buildx build --platform linux/amd64,linux/arm64 -t kubernetes_multi_unhealthy . --output type=docker`

Add tag.

`docker tag kubernetes_multi_unhealthy:latest kmi8000/kubernetes_multi_unhealthy:0.1.unhealthy`

Push image

`docker push kmi8000/kubernetes_multi_unhealthy:0.1.unhealthy`

The image is built to support multi platforms and avalable to download and use in **arm64** and **amd64** architectures.
