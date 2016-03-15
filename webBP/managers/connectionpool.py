import pymysql
import queue
import re
class ConnectionPool:
    def __init__(self, params, size):
        self.db_name = re.search('^([a-zA-Z]+://)?([0-9\.]+|[a-zA-Z]+)(:[0-9]+)?$', params.get('DATABASE')).groups()[1]
        self.port = int(params.get('PORT'))
        self.user = params.get('USER')
        self.password = params.get('PASSWORD')
        self.schema = params.get('SCHEMA')
        self.used_cons = 0
        self.num_of_cons = size
        self.cons = queue.Queue(size)
    def initialize_pool(self):
        for i in range(0,self.num_of_cons):
            connection = pymysql.connect(host=self.db_name, port=self.port, user=self.user, passwd=self.password,
                                         db=self.schema)
            self.cons.put(connection, block=False)

    def get_connection_from_pool(self):
        self.used_cons += 1
        return self.cons.get(block=False)

    def release_connection(self, c):
        self.cons.put(c, block=False)
        self.used_cons -= 1
