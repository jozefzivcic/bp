import pymysql
import logger

class UserManager:
    def __init__(self, con_pool):
        self.pool = con_pool
        self.logger = logger.Logger()

    def save_user(self, user):
        connection = None
        cur = None
        try:
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
            cur = connection.cursor()
            cur.execute('SELECT id FROM users WHERE user_name = %s;',(name))
            connection.commit()
            return cur.rowcount
        except pymysql.MySQLError as ex:
            self.logger.log_error('UserManager.get_users_with_name', ex)
            return -1
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def check_user_password(self, user):
        connection = None
        cur = None
        try:
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
