from http.server import BaseHTTPRequestHandler
from controller import index
from router import Router

class MyRequestHandler(BaseHTTPRequestHandler):

    """def __init__(self):
        self.router = Router()
        self.router.register_controller('/', index)"""
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        return
