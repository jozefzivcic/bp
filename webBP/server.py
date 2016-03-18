import os
import re
from http.server import HTTPServer

from jinja2 import FileSystemLoader, Environment

from controller import main_page
from managers.connectionpool import ConnectionPool
from myrequesthandler import MyRequestHandler
from configparser import ConfigParser
from router import Router

def load_texts():
    parser = ConfigParser()
    ret = {}
    texts_folder = 'views/texts'
    for file in os.listdir(texts_folder):
        res = re.search(r'^([a-z]+)[.][a-z]+$', file)
        language = res.groups()[0]
        parser.parse_file(os.path.join(texts_folder,file))
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
    router = Router()
    router.register_controller('/', main_page)
    MyRequestHandler.router = router
    env = Environment(loader=FileSystemLoader('views'))
    MyRequestHandler.environment = env
    MyRequestHandler.texts = load_texts()
    pool = ConnectionPool(extract_values_for_pool(parser), int(parser.get_key('POOLED_CONNECTIONS_FOR_WEB')))
    pool.initialize_pool()

if __name__ == '__main__':
    cp = ConfigParser()
    cp.parse_file('../config')
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