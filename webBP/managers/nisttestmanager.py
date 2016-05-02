from logger import Logger
import pymysql
from models.nistparam import NistParam


class NistTestManager:
    def __init__(self, pool):
        """
        Initializes class with pool and logger.
        :param pool: Connection pool for acquiring connection.
        """
        self.pool = pool
        self.logger = Logger()

    def store_nist_param(self, nist_param):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'INSERT INTO nist_tests (id_test, length, test_number, streams, special_parameter) VALUES (%s, %s, %s,%s,%s);',
                (nist_param.test_id, nist_param.length, nist_param.test_number, nist_param.streams,
                 nist_param.special_parameter))
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('NistTestManager.store_nist_param', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def get_nist_param_for_test(self, test):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'SELECT id_test, length, test_number, streams, special_parameter FROM nist_tests WHERE id_test = %s;',
                (test.id))
            connection.commit()
            nist_param = NistParam()
            i = 0
            for row in cur:
                nist_param.test_id = row[0]
                nist_param.length = row[1]
                nist_param.test_number = row[2]
                nist_param.streams = row[3]
                nist_param.special_parameter = row[4]
                i += 1
            if i == 1:
                return nist_param
            return None
        except pymysql.MySQLError as ex:
            self.logger.log_error('NistTestManager.get_nist_param_for_test', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def delete_nist_param_by_id(self, id):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('DELETE FROM nist_tests WHERE id_test = %s', (id))
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('NistTestManager.delete_nist_param_by_id', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)
