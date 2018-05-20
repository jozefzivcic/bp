import re
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

from jinja2 import FileSystemLoader, Environment
from os.path import dirname, abspath, join

from controllers.index_controller import index_get
from logger import Logger
from managers.connectionpool import ConnectionPool
from managers.currently_running_manager import CurrentlyRunningManager
from managers.dbtestmanager import DBTestManager
from managers.filemanager import FileManager
from managers.groupmanager import GroupManager
from managers.nisttestmanager import NistTestManager
from managers.pid_table_manager import PIDTableManager
from managers.resultsmanager import ResultsManager
from managers.sid_cookies_manager import SidCookiesManager
from managers.usermanager import UserManager


class MyRequestHandler(BaseHTTPRequestHandler):
    config_storage = None
    router = None
    texts = None
    path_to_users_dir = None
    not_authorised_paths = ['/wrong_user_name', '/wrong_password', '/sign_up', '/sign_up_user_exists',
                            '/sign_up_passwords_are_not_the_same', '/bootstrap/css/bootstrap.min.css',
                            '/styles.css', '/login', '/index.css', '/create_tests.js']

    def do_GET(self):
        """
        Handles HTTP GET request.
        :return: None.
        """
        self.pool = ConnectionPool(self.extract_values_for_pool(self.config_storage),
                                   self.config_storage.pooled_connections)
        self.prepare_objects()
        try:
            self.pool.initialize_pool()
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
        finally:
            self.pool.destroy_pool()
        return

    def do_POST(self):
        """
        Handles HTTP POST request.
        :return: None.
        """
        self.pool = ConnectionPool(self.extract_values_for_pool(self.config_storage),
                                   self.config_storage.pooled_connections)
        self.prepare_objects()
        try:
            self.pool.initialize_pool()
            self.sessions = self.get_cookies_dict()
            path = urlparse(self.path).path
            controller = self.router.get_controller(path)
            try:
                controller(self)
            except (FileNotFoundError, ValueError, KeyError) as e:
                self.logger.log_error('do_POST', e)
                controller = self.router.get_error_controller()
                controller(self)
        finally:
            self.pool.destroy_pool()
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

    def get_user_language(self, user_id):
        """
        Returns user preferred language according to user_id.
        :param user_id: Id of user.
        :return: String with language that is preferred by the user.
        """
        return 'en'

    def get_cookies_dict(self) -> dict:
        return self.cookie_manager.get_all_cookies()

    def add_new_cookies_for_user(self, user_id: int):
        return self.cookie_manager.add_new_cookies_for_user(user_id)

    def remove_from_cookies(self, sid: str):
        self.cookie_manager.remove_from_cookies(sid)

    def prepare_objects(self):
        env = Environment(loader=FileSystemLoader('views'))
        self.environment = env
        self.user_manager = UserManager(self.pool)
        self.test_manager = DBTestManager(self.pool)
        self.nist_manager = NistTestManager(self.pool)
        self.file_manager = FileManager(self.pool)
        self.results_manager = ResultsManager(self.pool)
        self.currently_running_manager = CurrentlyRunningManager(self.pool)
        self.group_manager = GroupManager(self.pool)
        self.pid_manager = PIDTableManager(self.pool)
        self.cookie_manager = SidCookiesManager(self.pool)
        self.logger = Logger()

    def extract_values_for_pool(self, config_storage):
        """
        Extracts values from config, that are needed for connection pool creation.
        :param config_storage: Object of type ConfigStorage().
        :return: Dictionary with values needed for ConnectionPool() creation.
        """
        res = re.search(r'^([a-zA-Z]+://)?([0-9\.]+|[a-zA-Z]+)[:]([0-9]+)?$', config_storage.database).groups()
        db = res[1]
        db_port = res[2]
        temp_dict = {'DATABASE': db,
                     'PORT': int(db_port),
                     'USERNAME': config_storage.user_name, 'USER_PASSWORD': config_storage.user_password,
                     'SCHEMA': config_storage.schema}
        return temp_dict
