from http.server import HTTPServer

from myrequesthandler import MyRequestHandler
import configparser

if __name__ == '__main__':
    cp = configparser.ConfigParser()
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