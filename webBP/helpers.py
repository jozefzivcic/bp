import os
import re
from os import makedirs, stat
from os.path import isdir, join
from hashlib import sha256
from pathlib import Path

from models.nistparam import NistParam
from managers.nisttestmanager import NistTestManager


def hash_password(password):
    return hash_file(password)


def render_login_template(handler, wrong_user, wrong_password):
    template = handler.environment.get_template('login.html')
    temp_dict = dict(handler.texts['en'])
    vars = {}
    vars['wrong_user'] = 1 if wrong_user else 0
    vars['wrong_password'] = 1 if wrong_password else 0
    temp_dict['vars'] = vars
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))


def render_signup_template(handler, user_already_exists, passwords_are_not_same):
    template = handler.environment.get_template('signup.html')
    temp_dict = dict(handler.texts['en'])
    vars = {}
    vars['user_already_exists'] = 1 if user_already_exists else 0
    vars['passwords_are_not_same'] = 1 if passwords_are_not_same else 0
    temp_dict['vars'] = vars
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))


def get_param_for_test(handler, test):
    if test.test_table == handler.config_storage.nist:
        nist_param = NistTestManager(handler.pool)
        return nist_param.get_nist_param_for_test(test)
    return None


def check_dir(path):
    return isdir(path)


def create_dir(path):
    makedirs(path)


def create_dir_if_not_exists(path):
    if not check_dir(path):
        create_dir(path)


def hash_file(file):
    if isinstance(file, str):
        return sha256(file.encode()).hexdigest()
    return sha256(file).hexdigest()


def get_file_size_in_bits(file):
    stats = stat(file)
    return stats.st_size * 8


def get_file_ids_from_nist_form(form):
    files = [file for file in form.keys() if file.startswith('file')]
    ids = []
    for file in files:
        file_id = re.search(r'file([0-9]+)', file).groups()[0]
        ids.append(int(file_id))
    return ids


def zip_folders(zip_class, arr):
    for folder in arr:
        for base, dirs, files in os.walk(folder):
            for file in files:
                file_name = os.path.join(base, file)
                p = Path(file_name).parent
                zip_class.write(file_name, join('/', p.name, file))
