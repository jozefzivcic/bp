import os
import re
from http.server import HTTPServer

from jinja2 import FileSystemLoader, Environment

from controller import index
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

def prepare_handler():
    router = Router()
    router.register_controller('/', index)
    MyRequestHandler.router = router
    env = Environment(loader=FileSystemLoader('views'))
    MyRequestHandler.environment = env
    MyRequestHandler.texts = load_texts()

if __name__ == '__main__':
    prepare_handler()
    cp = ConfigParser()
    cp.parse_file('../config')
    ip_address = cp.get_key('IP_ADDRESS')
    port = int(cp.get_key('PORT'))
    server_class = HTTPServer
    httpd = server_class((ip_address, port), MyRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()