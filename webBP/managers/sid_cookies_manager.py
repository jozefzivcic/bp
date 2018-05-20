import uuid

import pymysql

from logger import Logger


class SidCookiesManager(object):
    def __init__(self, pool):
        """
        Initializes class with pool and logger.
        :param pool: Connection pool for acquiring connection.
        """
        self.pool = pool
        self.logger = Logger()

    def get_all_cookies(self) -> dict:
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('SELECT sid_str, user_id FROM sid_cookies;')
            connection.commit()
            ret = {}
            for row in cur:
                ret[row[0]] = row[1]
            return ret
        except pymysql.MySQLError as ex:
            self.logger.log_error('SidCookiesManager.get_all_cookies', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def add_new_cookies_for_user(self, user_id: int) -> str:
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            generate_again = True
            sid = None
            while generate_again:
                sid = str(self.generate_sid())
                cur.execute('SELECT sid_str, user_id FROM sid_cookies WHERE sid_str = %s;', sid)
                if cur.rowcount < 1:
                    generate_again = False
            cur.execute('INSERT INTO sid_cookies (sid_str, user_id) VALUES (%s, %s);', (sid, user_id))
            connection.commit()
            return sid
        except pymysql.MySQLError as ex:
            self.logger.log_error('GroupManager.delete_test_from_group', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def remove_from_cookies(self, sid: str):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('DELETE FROM sid_cookies WHERE sid_str = %s;', sid)
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('SidCookiesManager.get_all_cookies', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def generate_sid(self):
        """
        Generates session identifier UUID.
        :return: Session identifier.
        """
        sid = uuid.uuid4()
        return sid
