from os import makedirs
from os.path import isdir
import os

from managers.nisttestmanager import NistTestManager


def hash_password(password):
    return password


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
    if test.test_table == handler.parser.get_key('NIST'):
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
    return file
