import pymysql

from logger import Logger


class ResultsManager:

    def __init__(self, pool):
        """
        Initializes class with pool and logger.
        :param pool: Connection pool for acquiring connection.
        """
        self.pool = pool
        self.logger = Logger()

    def get_path_for_test(self, test):
        """
        Returns directory where test's result are stored.
        :param test: Test which directory with results is searched for.
        :return: Path to directory with results or None if an error occurs.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
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

    def delete_result(self, test):
        """
        Deletes record from results table for test.
        :param test: Test which result is deleted.
        :return: If an error occurs False, True otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'DELETE FROM results WHERE id_test = %s;', (test.id))
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('ResultsManager.delete_result', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def get_paths_for_test_ids(self, test_ids: list):
        """
        Returns list of tuples. Each tuple consist of test_id and corresponding directory, where results for this test
        are stored.
        :param test_ids: ID's of tests which directories with results are searched for.
        :return: List of tuples or None if an error occurs.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            format_strings = ','.join(['%s'] * len(test_ids))
            cur.execute(
                'SELECT id_test, directory FROM results WHERE id_test IN (%s);' % format_strings, tuple(test_ids))
            connection.commit()
            ret = []
            for row in cur:
                ret.append((row[0], row[1]))
            return ret
        except pymysql.MySQLError as ex:
            self.logger.log_error('ResultsManager.get_paths_for_test_ids', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)
