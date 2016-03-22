from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import urlparse
import uuid


class MyRequestHandler(BaseHTTPRequestHandler):
    router = None
    environment = None
    texts = None
    sessions = {}
    pool = None
    user_manager = None
    test_manager = None
    file_manager = None
    not_authorised_paths = ['/wrong_user_name', '/wrong_password', '/sign_up', '/sign_up_user_exists',
                            '/sign_up_passwords_are_not_the_same']

    def do_GET(self):
        path = urlparse(self.path).path
        ckie = self.read_cookie()
        controller = None
        if (ckie == None) or (self.sessions.get(ckie) == None):
            if path in self.not_authorised_paths:
                controller = self.router.get_controller(path)
            else:
                controller = self.router.get_login_controller()
            controller(self)
            return
        controller = self.router.get_controller(path)
        controller(self)
        return

    def do_POST(self):
        path = urlparse(self.path).path
        controller = self.router.get_controller(path)
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
