from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie
import uuid


class MyRequestHandler(BaseHTTPRequestHandler):

    router = None
    environment = None
    texts = None
    sessions = {}
    pool = None
    user_manager = None

    def do_GET(self):
        ckie = self.read_cookie()
        controller = None
        if (ckie == None) or (self.sessions.get(ckie) == None):
            if (self.path == '/wrong_user_name') or (self.path == '/wrong_password'):
                controller = self.router.get_controller(self.path)
            else:
                controller = self.router.get_login_controller()
            controller(self)
            return
        controller = self.router.get_controller(self.path)
        controller(self)
        return

    def do_POST(self):
        controller = self.router.get_controller(self.path)
        controller(self)
        return

    def read_cookie(self):
        if "Cookie" in self.headers:
            v = self.headers['Cookie']
            c = SimpleCookie()
            c.load(v)
            value = c['sid'].value
            return value
        return None

    def write_cookie(self):
        c = SimpleCookie()
        sid = self.generate_sid()
        c['sid'] = sid
        self.send_header('Set-Cookie', c.output(header=''))
        return sid

    def generate_sid(self):
        sid = uuid.uuid4()
        return sid