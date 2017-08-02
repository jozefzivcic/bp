import pymysql
from models.test import Test
from logger import Logger


class DBTestManager:
    def __init__(self, pool):
        """
        Initializes class with pool and logger.
        :param pool: Connection pool for acquiring connection.
        """
        self.pool = pool
        self.logger = Logger()

    def get_tests_for_user(self, id):
        """
        Returns array of tests for user with id id.
        :param id: Id of user for whom tests are searched.
        :return: Array of tests or None if an error occurs.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'SELECT id, id_file, id_user, time_of_add, test_table, loaded, return_value, ended FROM tests WHERE id_user = %s;',
                (id))
            connection.commit()
            my_list = []
            for row in cur:
                test = Test()
                test.id = row[0]
                test.file_id = row[1]
                test.user_id = row[2]
                test.time_of_add = row[3]
                test.test_table = row[4]
                test.loaded = row[5]
                test.return_value = row[6]
                test.ended = row[7]
                my_list.append(test)
            return my_list
        except pymysql.MySQLError as ex:
            self.logger.log_error('DBTestManager.get_tests_for_user', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def store_test(self, test):
        """
        Saves test into database.
        :param test: Test to be saved.
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
                'INSERT INTO tests (id_file, id_user, test_table) VALUES(%s,%s,%s);',
                (test.file_id, test.user_id, test.test_table))
            test.id = cur.lastrowid
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('DBTestManager.store_test', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def get_test_for_user_by_id(self, user_id, test_id):
        """
        Returns test for user with id.
        :param user_id: Id of user.
        :param test_id: Id of test.
        :return: Test() or None if such test does not exist or an error occurs.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'SELECT id, id_file, id_user, time_of_add, test_table, loaded, return_value, ended FROM tests WHERE id = %s AND id_user = %s;',
                (test_id, user_id))
            connection.commit()
            i = 0
            test = Test()
            for row in cur:
                test.id = row[0]
                test.file_id = row[1]
                test.user_id = row[2]
                test.time_of_add = row[3]
                test.test_table = row[4]
                test.loaded = row[5]
                test.return_value = row[6]
                test.ended = row[7]
                i += 1
            if i == 1:
                return test
            return None
        except pymysql.MySQLError as ex:
            self.logger.log_error('DBTestManager.get_test_for_user_by_id', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def store_test_with_nist_param(self, test, nist_param, group_id):
        """
        Stores test and nist param atomically.
        :param test: Test to be saved.
        :param nist_param: NistParam() to be saved.
        :param group_id: Id of group into which test should be assigned.
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
                'INSERT INTO tests (id_file, id_user, test_table, group_id) VALUES(%s,%s,%s,%s);',
                (test.file_id, test.user_id, test.test_table, test.group_id))
            test.id = cur.lastrowid
            nist_param.test_id = test.id
            cur.execute(
                'INSERT INTO nist_tests (id_test, length, test_number, streams, special_parameter) VALUES (%s, %s, %s,%s,%s);',
                (nist_param.test_id, nist_param.length, nist_param.test_number, nist_param.streams,
                 nist_param.special_parameter))
            cur.execute('INSERT INTO groups_tests (id, id_test) VALUES(%s, %s)', (group_id, test.id))
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('DBTestManager.store_test_with_nist_param', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def get_tests_for_file(self, file):
        """
        Returns all tests that have assigned file.
        :param file: File() for which tests are searched.
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
                'SELECT id, id_file, id_user, time_of_add, test_table, loaded, return_value, ended FROM tests WHERE id_file = %s;',
                (file.id))
            connection.commit()
            arr = []
            for row in cur:
                test = Test()
                test.id = row[0]
                test.file_id = row[1]
                test.user_id = row[2]
                test.time_of_add = row[3]
                test.test_table = row[4]
                test.loaded = row[5]
                test.return_value = row[6]
                test.ended = row[7]
                arr.append(test)
            return arr
        except pymysql.MySQLError as ex:
            self.logger.log_error('DBTestManager.get_tests_for_file', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def delete_test(self, test):
        """
        Deletes selected test from database.
        :param test: Test to be deleted.
        :return: If an error occurs False, True otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('DELETE FROM tests WHERE id = %s', (test.id))
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('DBTestManager.delete_test', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)
