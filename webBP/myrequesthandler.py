import cgi
from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie
import uuid
from utils import hash_password

class MyRequestHandler(BaseHTTPRequestHandler):

    router = None
    environment = None
    texts = None
    sessions = {}
    pool = None

    def do_GET(self):
        ckie = self.read_cookie()
        controller = None
        if (ckie == None) or (self.sessions.get(ckie) == None):
            controller = self.router.get_login_controller()
            controller(self)
            return
        controller = self.router.get_controller(self.path)
        controller(self)
        return

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST',
                                                                              'CONTENT_TYPE':self.headers['Content-Type'],})
        user_name = form['username'].value
        password = form['password'].value
        if password == 'ahoj':
            self.send_response(303)
            self.send_header('Location','/')
            sid = self.write_cookie()
            self.end_headers()
            self.sessions[sid] = 1
        return

    def read_cookie(self):
        if "Cookie" in self.headers:
            c = SimpleCookie(self.headers["Cookie"])
        return c['sid'].value

    def write_cookie(self):
        c = SimpleCookie()
        sid = self.generate_sid()
        c['sid'] = sid
        self.send_header('Set-Cookie', c.output())
        return sid

    def generate_sid(self):
        sid = uuid.uuid4()
        return sid