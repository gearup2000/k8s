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
