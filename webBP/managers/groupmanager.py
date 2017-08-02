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
                'SELECT groups.id, id_user, time_of_add, id_test FROM groups INNER JOIN groups_tests ON groups.id = groups_tests.id WHERE id_user = %s;',
                (user_id))
            connection.commit()
            my_dict = {}
            for row in cur:
                group_id = row[0]
                if group_id in my_dict:
                    my_dict[group_id].test_id_arr.append(row[3])
                else:
                    group = Group()
                    group.id = group_id
                    group.user_id = row[1]
                    group.time_of_add = row[2]
                    group.test_id_arr.append(row[3])
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
        :return: If an error occurs None is returned, Group() object otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute(
                'SELECT groups.id, id_user, time_of_add, id_test FROM groups INNER JOIN groups_tests ON groups.id = groups_tests.id WHERE groups.id = %s AND id_user = %s;',
                (group_id, user_id))
            connection.commit()
            group = Group()
            group.id = None
            for row in cur:
                group_id = row[0]
                if group.id is None:
                    group.id = group_id
                    group.user_id = row[1]
                    group.time_of_add = row[2]
                    group.test_id_arr.append(row[3])
                elif group.id == group_id:
                    group.test_id_arr.append(row[3])
                else:
                    return None
            return group
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
