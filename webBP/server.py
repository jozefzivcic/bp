#!/usr/bin/python3.5
import os
import re
import signal
import ssl
from http.server import HTTPServer
from socketserver import ForkingMixIn

from configstorage import ConfigStorage
from controllers.common_controller import error_occurred
from controllers.compute_stats import compute_stats
from controllers.create_tests_controller import create_tests, create_tests_post
from controllers.css_controller import get_bootstrap, get_own_styles, get_index
from controllers.currently_running_controller import currently_running
from controllers.delete_file_controller import delete_file, delete_file_post
from controllers.delete_path_controller import delete_path, delete_path_post
from controllers.delete_test_controller import delete_test, delete_test_post
from controllers.file_controller import upload_file_post, upload_file
from controllers.group_tests_controller import get_tests_in_group, show_pdf_post
from controllers.groups_controller import get_groups, groups_download_post, get_download_report
from controllers.js_controller import get_js_create_tests
from controllers.login_controller import post_login, wrong_user_name, wrong_password, login
from controllers.main_controller import main_page, logout
from controllers.results_controller import results_controller, view_file_content
from controllers.sign_up_controller import sign_up, sign_up_user_exists, sign_up_passwords_are_not_the_same, \
    post_sign_up
from controllers.test_controller import test_controller
from helpers import create_dir_if_not_exists
from myconfigparser import MyConfigParser
from myrequesthandler import MyRequestHandler
from router import Router


def register_pages_into_router(router):
    """
    Creates mapping between URL and it's controller functions.
    :param router: Object of type Router().
    """
    router.register_controller('/', main_page)
    router.register_controller('/login', login)
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
    router.register_controller('/index.css', get_index)
    router.register_controller('/create_tests.js', get_js_create_tests)
    router.register_controller('/compute_stats', compute_stats)
    router.register_controller('/grp_results', get_download_report)
    router.register_controller('/groups/tests', get_tests_in_group)
    router.register_controller('/show_pdf', show_pdf_post)


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


def prepare_handler(config_storage):
    """
    Initializes MyRequestHandler with used objects inside this class.
    :param config_storage: ConfigStorage() object.
    """
    MyRequestHandler.config_storage = config_storage
    router = Router()
    register_pages_into_router(router)
    MyRequestHandler.router = router
    MyRequestHandler.texts = load_texts()
    MyRequestHandler.path_to_users_dir = os.path.abspath(config_storage.path_to_users_dir)


def prepare_environment(config_storage):
    """
    Creates file system structure.
    :param config_storage: ConfigStorage().
    """
    create_dir_if_not_exists(config_storage.path_to_users_dir)


class ForkHTTPServer(ForkingMixIn, HTTPServer):
    """Class for handling requests in a separate processes."""


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    cp = MyConfigParser()
    cp.parse_file('../config')
    config_storage = ConfigStorage(cp)
    prepare_environment(config_storage)
    ip_address = config_storage.ip_address
    port = config_storage.port
    prepare_handler(config_storage)
    server_class = ForkHTTPServer
    httpd = server_class((ip_address, port), MyRequestHandler)
    if ((config_storage.server_key != 'no') and
            (config_storage.server_cert != 'no') and (config_storage.ca_certs != 'no')):
        httpd.socket = ssl.wrap_socket(httpd.socket,
                                       keyfile=config_storage.server_key, certfile=config_storage.server_cert,
                                       server_side=True, ca_certs=config_storage.ca_certs)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
