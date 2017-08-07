import pymysql
from models.group import Group
from logger import Logger


class GroupManager:

    def __init__(self, pool):
        """
        Initializes class with pool and logger.
        :param pool: Connection pool for acquiring connection.
        """
        self.pool = pool;
        self.logger = Logger()

    def get_groups_for_user(self, user_id):
        """
        Returns all groups for user.
        :param user_id: Id of user for whom groups are searched.
        :return: If an error occurs None, else list of groups.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'SELECT groups.id, id_user, time_of_add, total_tests, finished_tests, stats, id_test FROM groups INNER JOIN groups_tests ON groups.id = groups_tests.id WHERE id_user = %s;',
                (user_id))
            connection.commit()
            my_dict = {}
            for row in cur:
                group_id = row[0]
                if group_id in my_dict:
                    my_dict[group_id].test_id_arr.append(row[6])
                else:
                    group = Group()
                    group.id = group_id
                    group.user_id = row[1]
                    group.time_of_add = row[2]
                    group.total_tests = row[3]
                    group.finished_tests = row[4]
                    group.stats = row[5]
                    group.test_id_arr.append(row[6])
                    my_dict[group_id] = group
            return list(my_dict.values())
        except pymysql.MySQLError as ex:
            self.logger.log_error('GroupManager.get_groups_for_user', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def get_group_by_id_for_user(self, group_id, user_id):
        """
        Returns group with id group_id for given user.
        :param group_id: Id of group which is searched.
        :param user_id: Id of user to whom group belongs.
        :return: If an error occurs None is returned. None is returned also, when user does not own group
         with group_id. Otherwise Group() object is returned.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'SELECT groups.id, id_user, time_of_add, total_tests, finished_tests, stats, id_test FROM groups INNER JOIN groups_tests ON groups.id = groups_tests.id WHERE groups.id = %s AND id_user = %s;',
                (group_id, user_id))
            connection.commit()
            group = Group()
            group.id = None
            i = 0
            for row in cur:
                i += 1
                group_id = row[0]
                if group.id is None:
                    group.id = group_id
                    group.user_id = row[1]
                    group.time_of_add = row[2]
                    group.total_tests = row[3]
                    group.finished_tests = row[4]
                    group.stats = row[5]
                    group.test_id_arr.append(row[6])
                elif group.id == group_id:
                    group.test_id_arr.append(row[6])
                else:
                    return None
            if i != 0:
                return group
            else:
                return None
        except pymysql.MySQLError as ex:
            self.logger.log_error('GroupManager.get_group_by_id_for_user', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def create_new_group(self, id_user):
        """
        Creates new group for user with id id_user.
        :param id_user: Id of user for whom new group is created.
        :return: If an error occurs None, else id of newly created group.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'INSERT INTO groups (id_user) VALUES(%s);', (id_user))
            group_id = cur.lastrowid
            connection.commit()
            return group_id
        except pymysql.MySQLError as ex:
            self.logger.log_error('GroupManager.create_new_group', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def delete_test_from_group(self, test):
        """
        Deletes given test from groups_tests table and if no record for test.group_id is in groups_tests, deletes group
        from groups also.
        :param test: test which is deleted from groups_tests.
        :return: If an error occurs False, True otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('SELECT id FROM groups_tests WHERE id_test = %s;', (test.id))
            group_id = None
            for row in cur:
                group_id = row[0]
            cur.execute('DELETE FROM groups_tests WHERE id_test = %s;', (test.id))
            cur.execute('SELECT id, id_test FROM groups_tests WHERE id = %s', (group_id))
            i = 0
            for row in cur:
                i += 1
                break
            if i < 1:
                cur.execute('DELETE FROM groups WHERE id = %s;', (group_id))
            else:
                cur.execute('UPDATE groups SET total_tests = total_tests - 1, finished_tests = finished_tests - 1 WHERE id = %s;', (group_id))
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('GroupManager.delete_test_from_group', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def set_num_of_tests(self, group_id, num):
        """
        Sets number of tests, that group contains.
        :param group_id: Id of group which group id should be set.
        :param num: Number of tests which group contains
        :return: If an error occurs False, True otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('UPDATE groups SET total_tests = %s WHERE groups.id = %s', (num, group_id))
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('GroupManager.set_num_of_tests', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def set_statistics_computed(self, group_id):
        """
        Sets attribute stats in table groups to 1. That means, that statistics for group of tests with id group_id
        is computed.
        :param group_id: Id of group which attribute stat should be set.
        :return: If an error occurs False, True otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('UPDATE groups SET stats = 1 WHERE groups.id = %s', (group_id))
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('GroupManager.set_statistics_computed', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def get_tests_for_group(self, group_id):
        """
        This function returns array of Test objects which are contained in group with id group_id.
        :param group_id: Id of group in which tests we are looking for belong.
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
                'SELECT tests.id, tests.id_file, tests.id_user, tests.time_of_add, tests.test_table, tests.loaded, '
                'tests.return_value, tests.ended FROM tests INNER JOIN groups_tests ON tests.id = groups_tests.id_test '
                'WHERE groups_tests.id = %s;',
                (group_id))
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
            self.logger.log_error('GroupManager.get_tests_for_group', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)
