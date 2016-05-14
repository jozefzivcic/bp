import os
import re
from http.server import HTTPServer
from socketserver import ThreadingMixIn

from jinja2 import FileSystemLoader, Environment

from myconfigparser import MyConfigParser
from configstorage import ConfigStorage
from controllers.css_controller import get_bootstrap, get_own_styles
from controllers.common_controller import error_occurred
from controllers.create_tests_controller import create_tests, create_tests_post
from controllers.currently_running_controller import currently_running
from controllers.delete_file_controller import delete_file, delete_file_post
from controllers.delete_path_controller import delete_path, delete_path_post
from controllers.delete_test_controller import delete_test, delete_test_post
from controllers.file_controller import upload_file_post, upload_file
from controllers.groups_controller import get_groups, groups_download_post
from controllers.login_controller import post_login, wrong_user_name, wrong_password
from controllers.main_controller import main_page, logout
from controllers.results_controller import results_controller, view_file_content
from controllers.sign_up_controller import sign_up, sign_up_user_exists, sign_up_passwords_are_not_the_same, \
    post_sign_up
from controllers.test_controller import test_controller
from helpers import create_dir_if_not_exists
from managers.connectionpool import ConnectionPool
from managers.currently_running_manager import CurrentlyRunningManager
from managers.dbtestmanager import DBTestManager
from managers.filemanager import FileManager
from managers.groupmanager import GroupManager
from managers.nisttestmanager import NistTestManager
from managers.pid_table_manager import PIDTableManager
from managers.resultsmanager import ResultsManager
from managers.usermanager import UserManager
from myrequesthandler import MyRequestHandler
from router import Router
from logger import Logger


def register_pages_into_router(router):
    """
    Creates mapping between URL and it's controller functions.
    :param router: Object of type Router().
    """
    router.register_controller('/', main_page)
    router.register_controller('/login_submit', post_login)
    router.register_controller('/logout', logout)
    router.register_controller('/wrong_user_name', wrong_user_name)
    router.register_controller('/wrong_password', wrong_password)
    router.register_controller('/sign_up', sign_up)
    router.register_controller('/sign_up_user_exists', sign_up_user_exists)
    router.register_controller('/sign_up_passwords_are_not_the_same', sign_up_passwords_are_not_the_same)
    router.register_controller('/sign_up_submit', post_sign_up)
    router.register_controller('/test', test_controller)
    router.register_controller('/test/results', results_controller)
    router.register_controller('/test/results/view', view_file_content)
    router.register_controller('/upload_file', upload_file)
    router.register_controller('/upload_file/upload', upload_file_post)
    router.register_controller('/create_tests', create_tests)
    router.register_controller('/create_tests_submit', create_tests_post)
    router.register_controller('/error', error_occurred)
    router.register_controller('/delete_path', delete_path)
    router.register_controller('/delete_fs_path_submit', delete_path_post)
    router.register_controller('/delete_file', delete_file)
    router.register_controller('/delete_file_submit', delete_file_post)
    router.register_controller('/delete_test', delete_test)
    router.register_controller('/delete_test_submit', delete_test_post)
    router.register_controller('/currently_running', currently_running)
    router.register_controller('/bootstrap/css/bootstrap.min.css', get_bootstrap)
    router.register_controller('/test/bootstrap/css/bootstrap.min.css', get_bootstrap)
    router.register_controller('/test/results/bootstrap/css/bootstrap.min.css', get_bootstrap)
    router.register_controller('/styles.css', get_own_styles)
    router.register_controller('/test/styles.css', get_own_styles)
    router.register_controller('/test/results/styles.css', get_own_styles)
    router.register_controller('/groups', get_groups)
    router.register_controller('/download', groups_download_post)


def load_texts():
    """
    Loads all texts from texts folder.
    :return: Dictionary with loaded texts.
    """
    parser = MyConfigParser()
    ret = {}
    texts_folder = 'views/texts'
    for file in os.listdir(texts_folder):
        res = re.search(r'^([a-z]+)[.][a-z]+$', file)
        language = res.groups()[0]
        parser.parse_file(os.path.join(texts_folder, file))
        ret[language] = parser.return_key_and_values()
    return ret


def extract_values_for_pool(config_storage):
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


def prepare_handler(config_storage):
    """
    Initializes MyRequestHandler with used objects inside this class.
    :param config_storage: ConfigStorage() object.
    """
    MyRequestHandler.config_storage = config_storage
    router = Router()
    register_pages_into_router(router)
    MyRequestHandler.router = router
    env = Environment(loader=FileSystemLoader('views'))
    MyRequestHandler.environment = env
    MyRequestHandler.texts = load_texts()
    pool = ConnectionPool(extract_values_for_pool(config_storage), config_storage.pooled_connections)
    pool.initialize_pool()
    MyRequestHandler.pool = pool
    MyRequestHandler.user_manager = UserManager(pool)
    MyRequestHandler.test_manager = DBTestManager(pool)
    MyRequestHandler.nist_manager = NistTestManager(pool)
    MyRequestHandler.file_manager = FileManager(pool)
    MyRequestHandler.results_manager = ResultsManager(pool)
    MyRequestHandler.currently_running_manager = CurrentlyRunningManager(pool)
    MyRequestHandler.group_manager = GroupManager(pool)
    MyRequestHandler.pid_manager = PIDTableManager(pool)
    MyRequestHandler.path_to_users_dir = os.path.abspath(config_storage.path_to_users_dir)
    MyRequestHandler.logger = Logger()


def prepare_environment(config_storage):
    """
    Creates file system structure.
    :param config_storage: ConfigStorage().
    """
    create_dir_if_not_exists(config_storage.path_to_users_dir)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Class for handling requests in a separate threads."""

if __name__ == '__main__':
    cp = MyConfigParser()
    cp.parse_file('../config')
    config_storage = ConfigStorage(cp)
    prepare_environment(config_storage)
    ip_address = config_storage.ip_address
    port = config_storage.port
    prepare_handler(config_storage)
    server_class = ThreadedHTTPServer
    httpd = server_class((ip_address, port), MyRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    MyRequestHandler.pool.destroy_pool()
