import pymysql
from models.test import Test
from logger import Logger


class DBTestManager:
    def __init__(self, pool):
        self.pool = pool
        self.logger = Logger()

    def get_tests_for_user(self, user):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'SELECT id, id_file, id_user, time_of_add, test_table, loaded, ended FROM tests WHERE id_user = %s;',
                (user.id))
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
                test.ended = row[6]
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
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'INSERT INTO tests (id, id_file, id_user, test_table) VALUES(%s,%s,%s,%s);',
                (test.id, test.file_id, test.user_id, test.test_table))
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
