import pymysql
from models.test import Test
from logger import Logger


class CurrentlyRunningManager:
    def __init__(self, pool):
        """
        Initializes class with pool and logger.
        :param pool: Connection pool for acquiring connection.
        """
        self.pool = pool
        self.logger = Logger()

    def get_running_tests_for_user(self, user_id):
        """
        Returns array of tests that are now running for given user.
        :param user_id:
        :return:
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'SELECT id, id_file, id_user, time_of_add, test_table, loaded, ended FROM tests INNER JOIN currently_running ON tests.id = currently_running.id_test WHERE id_user = %s;',
                (user_id))
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
            self.logger.log_error('CurrentlyRunningManager.get_running_tests_for_user', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)
