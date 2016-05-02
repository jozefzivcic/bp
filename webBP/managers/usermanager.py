import pymysql
import logger
from models.user import User


class UserManager:
    def __init__(self, con_pool):
        """
        Initializes class with pool and logger.
        :param con_pool: Connection pool for acquiring connection.
        """
        self.pool = con_pool
        self.logger = logger.Logger()

    def save_user(self, user):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('INSERT INTO users (user_name, user_password) VALUES (%s, %s);',(user.name, user.password))
            user.id = cur.lastrowid
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('UserManager.save_user', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def get_users_with_name(self, name):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('SELECT id, user_name, user_password FROM users WHERE user_name = %s;',(name))
            connection.commit()
            my_list = []
            for row in cur:
                user = User()
                user.id = row[0]
                user.name = row[1]
                user.password = row[2]
                my_list.append(user)
            return my_list
        except pymysql.MySQLError as ex:
            self.logger.log_error('UserManager.get_users_with_name', ex)
            return []
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def check_user_password(self, user):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('SELECT user_password FROM users WHERE user_name = %s;',(user.name))
            for row in cur:
                if row[0] == user.password:
                    return True
            return False
        except pymysql.MySQLError as ex:
            self.logger.log_error('UserManager.check_user_password', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)
