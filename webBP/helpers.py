import os
import re
from hashlib import sha256
from os import makedirs, stat
from os.path import isdir, join
from pathlib import Path

from managers.nisttestmanager import NistTestManager
from myrequesthandler import MyRequestHandler


def hash_password(password):
    """
    Creates hash of given parameter password.
    :param password: Password which hash is returned.
    :return: Hash.
    """
    return hash_file(password)


def render_login_template(handler, wrong_user, wrong_password):
    """
    Generates login page and writes it into handler.
    :param handler: MyRequestHandler.
    :param wrong_user: If wrong user name was given.
    :param wrong_password: If wrong user name was typed.
    """
    template = handler.environment.get_template('login.html')
    temp_dict = dict(handler.texts['en'])
    vars = {}
    vars['wrong_user'] = 1 if wrong_user else 0
    vars['wrong_password'] = 1 if wrong_password else 0
    temp_dict['vars'] = vars
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))


def render_signup_template(handler, user_already_exists, passwords_are_not_same):
    """
    Generates sign up page and writes it into handler.
    :param handler: MyRequestHandler
    :param user_already_exists: If user already exists and account with this name can't be created.
    :param passwords_are_not_same: If typed passwords re not the same.
    """
    template = handler.environment.get_template('signup.html')
    temp_dict = dict(handler.texts['en'])
    vars = {}
    vars['user_already_exists'] = 1 if user_already_exists else 0
    vars['passwords_are_not_same'] = 1 if passwords_are_not_same else 0
    temp_dict['vars'] = vars
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))


def get_param_for_test(handler, test):
    """
    Returns test parameter according to test type.
    :param handler: MyRequestHandler.
    :param test: Test to determine which table should be searched for.
    :return: If exists parameter for test, then parameter, else None.
    """
    if test.test_table == handler.config_storage.nist:
        nist_param = NistTestManager(handler.pool)
        return nist_param.get_nist_param_for_test(test)
    return None


def check_dir(path):
    """
    Checks if given path is directory.
    :param path: File system path to examine.
    :return: If given path is a directory, then True, False otherwise.
    """
    return isdir(path)


def create_dir(path):
    """
    Creates directory on given path.
    :param path: Filesystem path on which directory is created.
    """
    makedirs(path)


def create_dir_if_not_exists(path):
    """
    Creates directory if not exists.
    :param path: Directory.
    """
    if not check_dir(path):
        create_dir(path)


def hash_file(file):
    """
    Creates hash of given parameter file.
    :param file: Content of file from which hash is created and returned.
    :return: Hash of file - string or bytes.
    """
    if isinstance(file, str):
        return sha256(file.encode()).hexdigest()
    return sha256(file).hexdigest()


def get_file_size_in_bits(file):
    """
    Returns file size in bits of input file.
    :param file: File which size is returned.
    :return: File size in bits.
    """
    stats = stat(file)
    return stats.st_size * 8


def get_file_ids_from_nist_form(form):
    """
    Extracts all keys from form that start with file and parses number from each string.
    :param form: Form, that contains files.
    :return: File extracted id's.
    """
    files = [file for file in form.keys() if file.startswith('file')]
    ids = []
    for file in files:
        file_id = re.search(r'file([0-9]+)', file).groups()[0]
        ids.append(int(file_id))
    return ids


def zip_folders(zip_class, arr):
    """
    Creates .zip file of folders that are given as parameter arr.
    :param zip_class: Class ZipFile() that manages adding new files into .zip and creating it.
    :param arr: Array of folders which files are zipped.
    """
    for folder in arr:
        for base, dirs, files in os.walk(folder):
            for file in files:
                file_name = os.path.join(base, file)
                p = Path(file_name).parent
                zip_class.write(file_name, join('/', p.name, file))


def set_response_redirect(handler: MyRequestHandler, location: str):
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    handler.send_header('Location', location)
    handler.end_headers()


def set_response_not_found(handler: MyRequestHandler):
    set_response_redirect(handler, '/not_found')


def set_response_ok(handler: MyRequestHandler, content_type='text/html'):
    handler.send_response(200)
    handler.send_header('Content-type', content_type)
    handler.end_headers()


def get_params_for_tests(handler: MyRequestHandler, tests: list):
    if all(t.test_table == handler.config_storage.nist for t in tests):
        test_ids = [t.id for t in tests]
        return handler.nist_manager.get_nist_params_for_tests_list(test_ids)
    raise NotImplementedError('Param for test table is not defined')


def get_ids_of_elements_starting_with(form, prefix):
    elements = [element for element in form.keys() if element.startswith(prefix)]
    ids = []
    for element in elements:
        elem_id = re.search(prefix + r'([0-9]+)', element).groups()[0]
        ids.append(int(elem_id))
    return ids
