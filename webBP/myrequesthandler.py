from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import urlparse
import uuid

from controllers.index_controller import index_get


class MyRequestHandler(BaseHTTPRequestHandler):
    config_storage = None
    router = None
    environment = None
    texts = None
    sessions = {}
    pool = None
    user_manager = None
    test_manager = None
    nist_manager = None
    file_manager = None
    results_manager = None
    currently_running_manager = None
    group_manager = None
    pid_manager = None
    path_to_users_dir = None
    logger = None
    not_authorised_paths = ['/wrong_user_name', '/wrong_password', '/sign_up', '/sign_up_user_exists',
                            '/sign_up_passwords_are_not_the_same', '/bootstrap/css/bootstrap.min.css',
                            '/styles.css', '/login', '/index.css', '/create_tests.js']

    def do_GET(self):
        """
        Handles HTTP GET request.
        :return: None.
        """
        path = urlparse(self.path).path
        ckie = self.read_cookie()
        controller = None
        if (ckie is None) or (self.sessions.get(ckie) is None):
            if path == '/':
                controller = index_get
            elif path in self.not_authorised_paths:
                controller = self.router.get_controller(path)
            else:
                controller = self.router.get_login_controller()
            controller(self)
            return
        controller = self.router.get_controller(path)
        try:
            controller(self)
        except (FileNotFoundError, ValueError, KeyError) as e:
            self.logger.log_error('do_GET', e)
            controller = self.router.get_error_controller()
            controller(self)
        return

    def do_POST(self):
        """
        Handles HTTP POST request.
        :return: None.
        """
        path = urlparse(self.path).path
        controller = self.router.get_controller(path)
        try:
            controller(self)
        except (FileNotFoundError, ValueError, KeyError) as e:
            self.logger.log_error('do_POST', e)
            controller = self.router.get_error_controller()
            controller(self)
        return

    def read_cookie(self):
        """
        Reads cookie from HTTP headers.
        :return: Cookie with name sid - session id, or None if HTTP does not contains cookie.
        """
        if "Cookie" in self.headers:
            v = self.headers['Cookie']
            c = SimpleCookie()
            c.load(v)
            if 'sid' in c:
                value = c['sid'].value
                return value
        return None

    def write_cookie(self):
        """
        Generates and writes sid - session identifier into HTTP headers and returns value of sid.
        :return: Session identifier.
        """
        c = SimpleCookie()
        sid = self.generate_sid()
        while sid in self.sessions:
            sid = self.generate_sid()
        c['sid'] = sid
        self.send_header('Set-Cookie', c.output(header=''))
        return sid

    def generate_sid(self):
        """
        Generates session identifier UUID.
        :return: Session identifier.
        """
        sid = uuid.uuid4()
        return sid

    def get_user_language(self, user_id):
        """
        Returns user preferred language according to user_id.
        :param user_id: Id of user.
        :return: String with language that is preferred by the user.
        """
        return 'en'
