import os
import re
from http.server import HTTPServer

from jinja2 import FileSystemLoader, Environment

from configparser import ConfigParser
from controllers.file_controller import upload_file_post, upload_file
from controllers.login_controller import post_login, wrong_user_name, wrong_password
from controllers.main_controller import main_page, logout
from controllers.results_controller import results_controller, view_file_content
from controllers.sign_up_controller import sign_up, sign_up_user_exists, sign_up_passwords_are_not_the_same, \
    post_sign_up
from controllers.test_controller import test_controller
from helpers import create_dir_if_not_exists
from managers.connectionpool import ConnectionPool
from managers.dbtestmanager import DBTestManager
from managers.filemanager import FileManager
from managers.resultsmanager import ResultsManager
from managers.usermanager import UserManager
from myrequesthandler import MyRequestHandler
from router import Router


def register_pages_into_router(router):
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


def load_texts():
    parser = ConfigParser()
    ret = {}
    texts_folder = 'views/texts'
    for file in os.listdir(texts_folder):
        res = re.search(r'^([a-z]+)[.][a-z]+$', file)
        language = res.groups()[0]
        parser.parse_file(os.path.join(texts_folder, file))
        ret[language] = parser.return_key_and_values()
    return ret


def extract_values_for_pool(parser):
    res = re.search(r'^([a-zA-Z]+://)?([0-9\.]+|[a-zA-Z]+)[:]([0-9]+)?$', parser.get_key('DATABASE')).groups()
    db = res[1]
    db_port = res[2]
    temp_dict = {'DATABASE': db,
                 'PORT': int(db_port),
                 'USERNAME': parser.get_key('USERNAME'), 'USER_PASSWORD': parser.get_key('USER_PASSWORD'),
                 'SCHEMA': parser.get_key('SCHEMA')}
    return temp_dict


def prepare_handler(parser):
    MyRequestHandler.parser = parser
    router = Router()
    register_pages_into_router(router)
    MyRequestHandler.router = router
    env = Environment(loader=FileSystemLoader('views'))
    MyRequestHandler.environment = env
    MyRequestHandler.texts = load_texts()
    pool = ConnectionPool(extract_values_for_pool(parser), int(parser.get_key('POOLED_CONNECTIONS_FOR_WEB')))
    pool.initialize_pool()
    MyRequestHandler.pool = pool
    MyRequestHandler.user_manager = UserManager(pool)
    MyRequestHandler.test_manager = DBTestManager(pool)
    MyRequestHandler.file_manager = FileManager(pool)
    MyRequestHandler.results_manager = ResultsManager(pool)
    MyRequestHandler.path_to_users_dir = os.path.abspath(parser.get_key('PATH_TO_USERS_DIR_FROM_WEB'))


def prepare_environment(parser):
    create_dir_if_not_exists(parser.get_key('PATH_TO_USERS_DIR_FROM_WEB'))


if __name__ == '__main__':
    cp = ConfigParser()
    cp.parse_file('../config')
    prepare_environment(cp)
    ip_address = cp.get_key('IP_ADDRESS')
    port = int(cp.get_key('PORT'))
    prepare_handler(cp)
    server_class = HTTPServer
    httpd = server_class((ip_address, port), MyRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    MyRequestHandler.pool.destroy_pool()
