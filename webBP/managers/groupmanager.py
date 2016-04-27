import pymysql
from models.group import Group
from logger import Logger


class GroupManager:

    def __init__(self, pool):
        self.pool = pool;
        self.logger = Logger()

    def get_groups_for_user(self, user_id):
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
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('SELECT groups.id FROM groups INNER JOIN groups_tests ON groups.id = groups_tests.id WHERE id_test = %s;', (test.id))
            group_id = None
            for row in cur:
                group_id = row[0]
            cur.execute(
                'DELETE FROM groups_tests WHERE id_test = %s;', (test.id))
            cur.execute('SELECT groups.id, groups_tests.id_test FROM groups INNER JOIN groups_tests ON groups.id = groups_tests.id WHERE groups.id = %s', (group_id))
            i = 0
            for row in cur:
                i += 1
            if i < 1:
                cur.execute('DELETE FROM groups WHERE id = %s;', (group_id))
            connection.commit()
            return group_id
        except pymysql.MySQLError as ex:
            self.logger.log_error('GroupManager.create_new_group', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)
