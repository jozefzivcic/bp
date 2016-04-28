import pymysql

from logger import Logger


class PIDTableManager:

    def __init__(self, pool):
        self.pool = pool
        self.logger = Logger()

    def get_pid_by_id(self, table_id):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'SELECT pid FROM pid_table WHERE id = %s;', (table_id))
            connection.commit()
            i = 0
            pid = None
            for row in cur:
                pid = row[0]
                i += 1
            if i == 1:
                return pid
            return None
        except pymysql.MySQLError as ex:
            self.logger.log_error('PIDTableManager.get_pid_by_id', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)
