from os.path import join

import pymysql
from logger import Logger
from models.file import File


class FileManager:
    def __init__(self, pool):
        """
        Initializes class with pool and logger.
        :param pool: Connection pool for acquiring connection.
        """
        self.pool = pool
        self.logger = Logger()

    def save_file(self, file):
        """
        Saves file into database.
        :param file: File to be saved.
        :return: If an error occurs False, True otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('INSERT INTO files (id_user, hash, name, file_system_path) VALUES (%s, %s, %s, %s);',
                        (file.user_id, file.hash,
                         file.name, file.file_system_path))
            file.id = cur.lastrowid
            new_path = join(file.file_system_path, str(file.id))
            cur.execute('UPDATE files set file_system_path = %s WHERE id = %s', (new_path, file.id))
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
        """
        Returns file from database according to it's id.
        :param id: Id of file to search for.
        :return: If an error occurs, or in database is more than one file, then False, True otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
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
        """
        Returns dictionary with file.id as keys and file objects as values.
        :param user_id: Id of user which files are searched.
        :return: If an error occurs None, dictionary otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
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
        """
        Returns number of files for given user id with file_name as parameter.
        :param user_id: User id whose files are searched.
        :param file_name: Name of file, which is searched in database.
        :return: Number of files, or -1 if an error occurs.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
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

    def get_existing_files_for_user(self, user_id):
        """
        Returns dictionary of all files for user with user id user_id, that are present in system - their
        file_system_path is not NULL. Keys are represented with file.id and values with file objects - File().
        :param user_id: Id of user which files are searched.
        :return: If an error occurs None, dictionary otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('SELECT id, id_user, hash, name, file_system_path FROM files WHERE id_user = %s AND file_system_path IS NOT NULL;', (user_id))
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
            self.logger.log_error('FileManager.get_existing_files_for_user', ex)
            return None
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def set_fs_path_to_null(self, file):
        """
        Sets attribute file.file_system_path to NULL.
        :param file: File which path is set to NULL.
        :return: If an error occurs False, True otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('UPDATE files SET file_system_path = NULL WHERE id = %s;', (file.id))
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('FileManager.get_files_for_user', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)

    def delete_file(self, file):
        """
        Deletes file from database.
        :param file: File to be deleted.
        :return: If an error occurs False, True otherwise.
        """
        connection = None
        cur = None
        try:
            connection = self.pool.get_connection_from_pool()
            while connection is None:
                connection = self.pool.get_connection_from_pool()
            cur = connection.cursor()
            cur.execute('DELETE FROM files WHERE id = %s;', (file.id))
            connection.commit()
            return True
        except pymysql.MySQLError as ex:
            self.logger.log_error('FileManager.delete_file', ex)
            return False
        finally:
            if cur:
                cur.close()
            self.pool.release_connection(connection)
