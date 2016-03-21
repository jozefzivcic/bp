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
    not_authorised_paths = ['/wrong_user_name', '/wrong_password', '/sign_up', '/sign_up_user_exists',
                            '/sign_up_passwords_are_not_the_same']

    def do_GET(self):
        ckie = self.read_cookie()
        controller = None
        if (ckie == None) or (self.sessions.get(ckie) == None):
            if self.path in self.not_authorised_paths:
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
