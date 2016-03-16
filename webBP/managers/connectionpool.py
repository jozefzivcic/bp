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
            connection = self.create_connection()
            self.cons.put(connection, block=False)

    def destroy_pool(self):
        for i in range(0, self.num_of_cons):
            if not self.cons.empty():
                connection = self.cons.get(block=False)
                connection.close()

    def get_connection_from_pool(self):
        self.used_cons += 1
        connection = self.cons.get(block=False)
        if not self.ping_connection(connection):
            connection = self.create_connection()
        return connection

    def release_connection(self, c):
        if c:
            self.cons.put(c, block=False)
            self.used_cons -= 1

    def create_connection(self):
        return pymysql.connect(host=self.db_name, port=self.port, user=self.user, passwd=self.password,
                                         db=self.schema)
    def ping_connection(self, conn):
        cur = None
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1;")
            return True
        except (AttributeError, pymysql.OperationalError):
            return False
        finally:
            cur.close()
