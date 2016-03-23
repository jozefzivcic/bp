import pymysql

from logger import Logger


class ResultsManager:

    def __init__(self, pool):
        self.pool = pool
        self.logger = Logger()

    def get_path_for_test(self, test):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'SELECT directory FROM results WHERE id_test = %s;', (test.id))
            connection.commit()
            path = None
            for row in cur:
                path = row[0]
            return path
        except pymysql.MySQLError as ex:
            self.logger.log_error('ResultsManager.get_path_for_test', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)