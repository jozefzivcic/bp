import cgi
import re
from os import makedirs, stat
from os.path import isdir, join
from hashlib import sha256

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
    if isinstance(file, str):
        return sha256(file.encode()).hexdigest()
    return sha256(file).hexdigest()


def get_file_size_in_bits(file):
    stats = stat(file)
    return stats.st_size * 8


def create_nist_param_from_nist_form(form, length, streams, block_size=None):
    param = NistParam()
    if length in form:
        param.length = form[length].value
    else:
        param.length = None
    if streams in form:
        param.streams = form[streams].value
    else:
        param.streams = 1
    if block_size is not None:
        if block_size in form:
            param.special_parameter = form[block_size].value
        #else:
        #    param.special_parameter =
        return tuple(length, streams, param)
    return tuple(length, streams)


def parse_nist_form(handler):
    temp_dict = {}
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    if 'frequency' in form:
        temp_dict[1] = create_nist_param_from_nist_form(form, 'frequency_length', 'frequency_streams')
    elif 'block_frequency' in form:
        temp_dict[2] = create_nist_param_from_nist_form(form, 'block_frequency_length', 'block_frequency_streams',
                                                   'block_frequency_param')
    elif 'cumulative_sums' in form:
        temp_dict[3] = create_nist_param_from_nist_form(form, 'cumulative_sums_length', 'cumulative_sums_streams')
    elif 'runs' in form:
        temp_dict[4] = create_nist_param_from_nist_form(form, 'runs_length', 'runs_streams')
    elif 'longest_run_of_ones' in form:
        temp_dict[5] = create_nist_param_from_nist_form(form, 'longest_run_of_ones_length', 'longest_run_of_ones_streams')
    elif 'rank' in form:
        temp_dict[6] = create_nist_param_from_nist_form(form, 'rank_length', 'rank_streams')
    elif 'discrete_fourier_transform' in form:
        temp_dict[7] = create_nist_param_from_nist_form(form, 'discrete_fourier_transform_length',
                                                   'discrete_fourier_transform_streams')
    elif 'nonperiodic' in form:
        temp_dict[8] = create_nist_param_from_nist_form(form, 'nonperiodic_length', 'nonperiodic_streams',
                                                   'nonperiodic_param')
    elif 'overlapping' in form:
        temp_dict[9] = create_nist_param_from_nist_form(form, 'overlapping_length', 'overlapping_streams',
                                                   'overlapping_param')
    elif 'universal' in form:
        temp_dict[10] = create_nist_param_from_nist_form(form, 'universal_length', 'universal_streams')
    elif 'apen' in form:
        temp_dict[11] = create_nist_param_from_nist_form(form, 'apen_length', 'apen_streams', 'apen_param')
    elif 'excursion' in form:
        temp_dict[12] = create_nist_param_from_nist_form(form, 'excursion_length', 'excursion_streams')
    elif 'excursion_var' in form:
        temp_dict[13] = create_nist_param_from_nist_form(form, 'excursion_var_length', 'excursion_var_streams')
    elif 'serial' in form:
        temp_dict[14] = create_nist_param_from_nist_form(form, 'serial_length', 'serial_streams', 'serial_param')
    elif 'linear' in form:
        temp_dict[15] = create_nist_param_from_nist_form(form, 'linear_length', 'linear_streams', 'linear_param')
    return temp_dict


def get_file_ids_from_nist_form(handler):
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    files = [file for file in form.keys() if file.startswith('file')]
    ids = []
    for file in files:
        file_id = re.search(r'file([0-9]+)', file).groups()[0]
        ids.append(int(file_id))
    return ids


def control_forms(handler, file_ids, my_dict):
    user_dir = join(handler.path_to_users_dir, str(id),handler.parser.get_key('FILES'))

    return 0
