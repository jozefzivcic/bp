import re
from os import makedirs, stat
from os.path import isdir, join
from hashlib import sha256
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


def create_nist_param_from_nist_form(form, test, length, streams, block_size=None):
    param = NistParam()
    param.test_number = test
    if length in form:
        param.length = int(form[length].value)
    else:
        param.length = None
    if streams in form:
        param.streams = int(form[streams].value)
    else:
        param.streams = 1
    if block_size is not None:
        if block_size in form:
            param.special_parameter = int(form[block_size].value)
        else:
            param.set_default_param_value_according_to_test()
    return param


def parse_nist_form(form):
    arr = []
    if 'frequency' in form:
        arr.append(create_nist_param_from_nist_form(form, 1, 'frequency_length', 'frequency_streams'))
    if 'block_frequency' in form:
        arr.append(create_nist_param_from_nist_form(form, 2, 'block_frequency_length', 'block_frequency_streams',
                                                    'block_frequency_param'))
    if 'cumulative_sums' in form:
        arr.append(create_nist_param_from_nist_form(form, 3, 'cumulative_sums_length', 'cumulative_sums_streams'))
    if 'runs' in form:
        arr.append(create_nist_param_from_nist_form(form, 4, 'runs_length', 'runs_streams'))
    if 'longest_run_of_ones' in form:
        arr.append(
            create_nist_param_from_nist_form(form, 5, 'longest_run_of_ones_length', 'longest_run_of_ones_streams'))
    if 'rank' in form:
        arr.append(create_nist_param_from_nist_form(form, 6, 'rank_length', 'rank_streams'))
    if 'discrete_fourier_transform' in form:
        arr.append(create_nist_param_from_nist_form(form, 7, 'discrete_fourier_transform_length',
                                                    'discrete_fourier_transform_streams'))
    if 'nonperiodic' in form:
        arr.append(create_nist_param_from_nist_form(form, 8, 'nonperiodic_length', 'nonperiodic_streams',
                                                    'nonperiodic_param'))
    if 'overlapping' in form:
        arr.append(create_nist_param_from_nist_form(form, 9, 'overlapping_length', 'overlapping_streams',
                                                    'overlapping_param'))
    if 'universal' in form:
        arr.append(create_nist_param_from_nist_form(form, 10, 'universal_length', 'universal_streams'))
    if 'apen' in form:
        arr.append(create_nist_param_from_nist_form(form, 11, 'apen_length', 'apen_streams', 'apen_param'))
    if 'excursion' in form:
        arr.append(create_nist_param_from_nist_form(form, 12, 'excursion_length', 'excursion_streams'))
    if 'excursion_var' in form:
        arr.append(create_nist_param_from_nist_form(form, 13, 'excursion_var_length', 'excursion_var_streams'))
    if 'serial' in form:
        arr.append(create_nist_param_from_nist_form(form, 14, 'serial_length', 'serial_streams', 'serial_param'))
    if 'linear' in form:
        arr.append(create_nist_param_from_nist_form(form, 15, 'linear_length', 'linear_streams', 'linear_param'))
    return arr


def get_file_ids_from_nist_form(form):
    files = [file for file in form.keys() if file.startswith('file')]
    ids = []
    for file in files:
        file_id = re.search(r'file([0-9]+)', file).groups()[0]
        ids.append(int(file_id))
    return ids


def control_nist_forms(handler, user_id, file_ids, nist_params):
    user_dir = join(handler.path_to_users_dir, str(user_id), handler.config_storage.files)
    if len(file_ids) == 0:
        return (4,0)
    if len(nist_params) == 0:
        return (5,0)
    for file_id in file_ids:
        file_path = join(user_dir, str(file_id))
        size = get_file_size_in_bits(file_path)
        for param in nist_params:
            if param.length is None:
                return (6, param.test_number)
            elif param.length > size:
                return (1, param.test_number)
            if param.streams < 1:
                return (2, param.test_number)
            if (param.special_parameter is not None) and (param.special_parameter < 1):
                return (3, param.test_number)
    return (0, 0)
