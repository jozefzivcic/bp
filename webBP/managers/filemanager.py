import pymysql
from logger import Logger
from models.file import File


class FileManager:
    def __init__(self, pool):
        self.pool = pool
        self.logger = Logger()

    def save_file(self, file):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('INSERT INTO files (id_user, hash, name, file_system_path) VALUES (%s, %s, %s, %s);',
                        (file.user_id, file.hash,
                         file.name, file.file_system_path))
            file.id = cur.lastrowid
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('FileManager.save_file', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def get_file_by_id(self, id):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('SELECT id, id_user, hash, name, file_system_path FROM files WHERE id = %s;', (id))
            connection.commit()
            file = File()
            i = 0
            for row in cur:
                file.id = row[0]
                file.user_id = row[1]
                file.hash = row[2]
                file.name = row[3]
                file.file_system_path = row[4]
                i += 1
            if i == 1:
                return file
            return None
        except pymysql.MySQLError as ex:
            self.logger.log_error('FileManager.get_file_by_id', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def get_files_for_user(self, user_id):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('SELECT id, id_user, hash, name, file_system_path FROM files WHERE id_user = %s;', (user_id))
            connection.commit()
            temp_dict = {}
            for row in cur:
                file = File()
                file.id = row[0]
                file.user_id = row[1]
                file.hash = row[2]
                file.name = row[3]
                file.file_system_path = row[4]
                temp_dict[file.id] = file
            return temp_dict
        except pymysql.MySQLError as ex:
            self.logger.log_error('FileManager.get_files_for_user', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def get_num_of_files_with_name_for_user(self, user_id, file_name):
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('SELECT id FROM files WHERE id_user = %s AND name = %s;', (user_id, file_name))
            connection.commit()
            i = 0
            for row in cur:
                i += 1
            return i
        except pymysql.MySQLError as ex:
            self.logger.log_error('FileManager.get_files_for_user', ex)
            return -1
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)
