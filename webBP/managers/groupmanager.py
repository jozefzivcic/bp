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