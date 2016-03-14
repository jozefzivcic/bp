from http.server import BaseHTTPRequestHandler, HTTPServer

from myrequesthandler import MyRequestHandler

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class(("127.0.0.1","8080"),MyRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
