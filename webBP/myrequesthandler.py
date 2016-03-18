from http.server import BaseHTTPRequestHandler
from controller import index
from router import Router


class MyRequestHandler(BaseHTTPRequestHandler):

    router = None
    environment = None
    texts = None

    def do_GET(self):
        controller = self.router.get_controller(self.path)
        controller(self)
        return
