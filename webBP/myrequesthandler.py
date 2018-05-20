import pickle
from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from os.path import dirname, abspath, join, exists
from urllib.parse import urlparse
import uuid

from controllers.index_controller import index_get


this_dir = dirname(abspath(__file__))
cookies_file = join(this_dir, 'cookies_file')


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
        self.sessions = self.get_cookies_dict()
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
        self.sessions = self.get_cookies_dict()
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

    def write_cookie(self, sid):
        """
        Generates and writes sid - session identifier into HTTP headers and returns value of sid.
        :return: Session identifier.
        """
        c = SimpleCookie()
        c['sid'] = sid
        self.send_header('Set-Cookie', c.output(header=''))

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

    def get_cookies_dict(self) -> dict:
        if not exists(cookies_file):
            return {}
        with open(cookies_file, 'rb') as f:
            cookies = pickle.load(f)
        return cookies

    def add_new_cookies_for_user(self, user_id: int):
        cookies = self.get_cookies_dict()
        sid = str(self.generate_sid())
        while sid in cookies:
            sid = str(self.generate_sid())
        cookies[sid] = user_id
        with open(cookies_file, 'wb') as f:
            pickle.dump(cookies, f, pickle.HIGHEST_PROTOCOL)
        return sid

    def remove_from_cookies(self, sid: str):
        cookies = self.get_cookies_dict()
        del cookies[sid]
        with open(cookies_file, 'wb') as f:
            pickle.dump(cookies, f, pickle.HIGHEST_PROTOCOL)
