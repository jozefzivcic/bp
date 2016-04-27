import pymysql
import queue
import re
import logger
from threading import Lock


class ConnectionPool:
    def __init__(self, params, size):
        self.db_name = params.get('DATABASE')
        self.port = params.get('PORT')
        self.user = params.get('USERNAME')
        self.password = params.get('USER_PASSWORD')
        self.schema = params.get('SCHEMA')
        self.used_cons = 0
        self.num_of_cons = size
        self.cons = queue.Queue(size)
        self.logger = logger.Logger()
        self.mut = Lock()

    def initialize_pool(self):
        for i in range(0, self.num_of_cons):
            connection = self.create_connection()
            self.cons.put(connection, block=False)

    def destroy_pool(self):
        for i in range(0, self.num_of_cons):
            if not self.cons.empty():
                connection = self.cons.get(block=False)
                connection.close()

    def get_connection_from_pool(self):
        try:
            self.mut.acquire()
            if self.used_cons >= self.num_of_cons:
                return None
            self.used_cons += 1
            connection = self.cons.get(block=False)
            if not self.ping_connection(connection):
                connection = self.create_connection()
            return connection
        finally:
            self.mut.release()

    def release_connection(self, c):
        if not c:
            return None
        try:
            self.mut.acquire()
            self.cons.put(c, block=False)
            self.used_cons -= 1
        finally:
            self.mut.release()

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
            self.logger.log_info('ConnectionPool.ping_connection: connection closed')
            return False
        finally:
            cur.close()
