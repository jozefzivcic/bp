import cgi
import os
import signal
from math import log
from os.path import join
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qs
from models.test import Test
from helpers import get_file_ids_from_nist_form, get_file_size_in_bits
from models.nistparam import NistParam
from enums import CreateErrors


def create_tests(handler):
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)
    parsed_queries = parse_queries(queries)
    if parsed_queries is None:
        handler.send_response(303)
        handler.send_header('Content-type', 'text/html')
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    user_id = handler.sessions[handler.read_cookie()]
    files = handler.file_manager.get_existing_files_for_user(user_id).values()
    template = handler.environment.get_template('create_tests.html')
    temp_dict = dict(handler.texts['en'])
    temp_dict['vars'] = {}
    temp_dict['vars']['files'] = files
    temp_dict['vars']['queries'] = parsed_queries
    if (parsed_queries is not None) and ('files' in parsed_queries):
        temp_dict['vars']['file_ids'] = get_int_array_from_string(parsed_queries.get('files'))
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def create_tests_post(handler):
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    file_ids = get_file_ids_from_nist_form(form)
    test_error = None
    ret = None
    nist_params = parse_nist_form(form)
    user_id = handler.sessions[handler.read_cookie()]
    if nist_params[1] is None:
        ret = control_nist_forms(handler, user_id, file_ids, nist_params[0])
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    if ret != (CreateErrors.ok, 0):
        length = None
        streams = None
        if 'length' in form:
            length = int(form['length'].value)
        if 'streams' in form:
            streams = int(form['streams'].value)
        qstr = convert_nist_form_params_to_query(file_ids, nist_params[0], length, streams)
        if nist_params[1] is not None:
            qstr += '&format=1&t=' + str(nist_params[1])
        elif ret[0] == CreateErrors.length_greater_than_size:
            qstr += '&l=1&t=' + str(ret[1])
        elif ret[0] == CreateErrors.streams_less_than_one:
            qstr += '&s=1&t=' + str(ret[1])
        elif ret[0] == CreateErrors.special_param_not_in_range:
            qstr += '&p=1&t=' + str(ret[1])
        elif ret[0] == CreateErrors.length_files:
            qstr += '&f=1'
        elif ret[0] == CreateErrors.length_params_array:
            qstr += '&test=1'
        elif ret[0] == CreateErrors.length_none:
            qstr += '&l=2&t=' + str(ret[1])
        location = '/create_tests?' + qstr
        handler.send_header('Location', location)
        handler.end_headers()
        return

    t = Test()
    t.user_id = user_id
    t.test_table = handler.config_storage.nist
    group_id = handler.group_manager.create_new_group(user_id)
    for file_id in file_ids:
        t.file_id = file_id
        for nist_param in nist_params[0]:
            handler.test_manager.store_test_with_nist_param(t, nist_param, group_id)
    handler.send_header('Location', '/')
    handler.end_headers()
    pid = handler.pid_manager.get_pid_by_id(handler.config_storage.sched_id_of_pid)
    os.kill(pid, signal.SIGUSR1)
    return


def get_possible_keys_and_values():
    arr = {'l': str, 't': int, 'p': int, 'frequency': int, 'block_frequency': int, 'block_frequency_param': str,
           'cumulative_sums': int, 'runs': int, 'longest_run_of_ones': int, 'rank': int,
           'discrete_fourier_transform': int, 'nonperiodic': int, 'nonperiodic_param': str, 'overlapping': int,
           'overlapping_param': str, 'universal': int, 'apen': int, 'apen_param': str, 'excursion': int,
           'excursion_var': int, 'serial': int, 'serial_param': str, 'linear': int, 'linear_param': str, 'f': int,
           'test': int, 'files': str, 'length': int, 'streams': int, 'nonperiodic2': int, 'nonperiodic3': int,
           'nonperiodic4': int, 'nonperiodic5': int, 'nonperiodic6': int, 'nonperiodic7': int, 'nonperiodic8': int,
           'nonperiodic9': int, 'nonperiodic10': int, 'nonperiodic11': int, 'nonperiodic12': int, 'nonperiodic13': int,
           'nonperiodic14': int, 'nonperiodic15': int, 'nonperiodic16': int, 'nonperiodic17': int, 'nonperiodic18': int,
           'nonperiodic19': int, 'nonperiodic20': int, 'nonperiodic21': int, 'format': int}
    return arr


def parse_queries(queries):
    possible = get_possible_keys_and_values()
    possible_keys = list(possible.keys())
    temp_dict = {}
    for key in queries.keys():
        if key not in possible_keys:
            return None
        elif possible[key] == int:
            try:
                i = int(queries[key][0])
                if i < 0:
                    return None
                temp_dict[key] = i
            except ValueError:
                return None
        elif isinstance(queries[key][0], possible[key]):
            if key == 'nonperiodic_param':
                try:
                    my_arr = get_int_array_from_string(queries[key][0])
                except ValueError:
                    return None
                temp_dict[key] = my_arr
            else:
                temp_dict[key] = queries[key][0]
        else:
            return None
    return temp_dict


def convert_nist_form_params_to_query(file_ids, params, length, streams):
    temp_dict = {}
    encoded_ids = get_string_from_int_array(file_ids)
    temp_dict['files'] = encoded_ids
    if length is not None:
        temp_dict['length'] = length
    if streams is not None:
        temp_dict['streams'] = streams
    param_values = {}
    if params is None:
        return ''
    for param in params:
        cb_name = get_checkbox_name(param.test_number)
        param_name = get_param_name(param.test_number)
        temp_dict[cb_name] = 1
        if param_name is not None:
            if param_name in param_values:
                param_values[param_name].append(param.special_parameter)
            else:
                param_values[param_name] = []
                param_values[param_name].append(param.special_parameter)
    for key in param_values.keys():
        temp_dict[key] = get_string_from_int_array(param_values[key])
    return urlencode(temp_dict)


def get_checkbox_name(test_number):
    if test_number == 1:
        return 'frequency'
    elif test_number == 2:
        return 'block_frequency'
    elif test_number == 3:
        return 'cumulative_sums'
    elif test_number == 4:
        return 'runs'
    elif test_number == 5:
        return 'longest_run_of_ones'
    elif test_number == 6:
        return 'rank'
    elif test_number == 7:
        return 'discrete_fourier_transform'
    elif test_number == 8:
        return 'nonperiodic'
    elif test_number == 9:
        return 'overlapping'
    elif test_number == 10:
        return 'universal'
    elif test_number == 11:
        return 'apen'
    elif test_number == 12:
        return 'excursion'
    elif test_number == 13:
        return 'excursion_var'
    elif test_number == 14:
        return 'serial'
    elif test_number == 15:
        return 'linear'
    return None


def get_param_name(test_number):
    if test_number == 2:
        return 'block_frequency_param'
    elif test_number == 8:
        return 'nonperiodic_param'
    elif test_number == 9:
        return 'overlapping_param'
    elif test_number == 11:
        return 'apen_param'
    elif test_number == 14:
        return 'serial_param'
    elif test_number == 15:
        return 'linear_param'
    return None


def get_string_from_int_array(arr):
    return str(arr).strip('[]')


def get_int_array_from_string(str_param):
    temp_arr = str_param.split(',')
    ret_array = [int(num) for num in temp_arr]
    return ret_array


def create_nist_param_from_nist_form(test, length, streams, block_size=None):
    param = NistParam()
    param.test_number = test
    param.length = length
    param.streams = streams
    if block_size is not None:
        param.special_parameter = block_size
    return param


def parse_nist_form(form):
    arr = []
    ret = None
    if 'length' in form:
        length = int(form['length'].value)
    else:
        length = None
    if 'streams' in form:
        streams = int(form['streams'].value)
    else:
        streams = 1
    if 'frequency' in form:
        arr.append(create_nist_param_from_nist_form(1, length, streams))
    if 'block_frequency' in form:
        temp = fill_array_from_text_input(arr, form, length, streams, 2, 'block_frequency_param')
        if ret is None and not temp:
            ret = 2
    if 'cumulative_sums' in form:
        arr.append(create_nist_param_from_nist_form(3, length, streams))
    if 'runs' in form:
        arr.append(create_nist_param_from_nist_form(4, length, streams))
    if 'longest_run_of_ones' in form:
        arr.append(create_nist_param_from_nist_form(5, length, streams))
    if 'rank' in form:
        arr.append(create_nist_param_from_nist_form(6, length, streams))
    if 'discrete_fourier_transform' in form:
        arr.append(create_nist_param_from_nist_form(7, length, streams))
    if 'nonperiodic' in form:
        fill_array_from_checkboxes(arr, form, length, streams, 8, 'nonperiodic', 2, 22)
    if 'overlapping' in form:
        temp = fill_array_from_text_input(arr, form, length, streams, 9, 'overlapping_param')
        if ret is None and not temp:
            ret = 9
    if 'universal' in form:
        arr.append(create_nist_param_from_nist_form(10, length, streams))
    if 'apen' in form:
        temp = fill_array_from_text_input(arr, form, length, streams, 11, 'apen_param')
        if ret is None and not temp:
            ret = 11
    if 'excursion' in form:
        arr.append(create_nist_param_from_nist_form(12, length, streams))
    if 'excursion_var' in form:
        arr.append(create_nist_param_from_nist_form(13, length, streams))
    if 'serial' in form:
        temp = fill_array_from_text_input(arr, form, length, streams, 14, 'serial_param')
        if ret is None and not temp:
            ret = 14
    if 'linear' in form:
        temp = fill_array_from_text_input(arr, form, length, streams, 15, 'linear_param')
        if ret is None and not temp:
            ret = 15
    return arr, ret


def control_nist_forms(handler, user_id, file_ids, nist_params):
    user_dir = join(handler.path_to_users_dir, str(user_id), handler.config_storage.files)
    if len(file_ids) == 0:
        return (CreateErrors.length_files, 0)
    if len(nist_params) == 0:
        return (CreateErrors.length_params_array, 0)
    for file_id in file_ids:
        file_path = join(user_dir, str(file_id))
        size = get_file_size_in_bits(file_path)
        for param in nist_params:
            if param.length is None:
                return (CreateErrors.length_none, param.test_number)
            elif param.streams < 1:
                return (CreateErrors.streams_less_than_one, param.test_number)
            elif param.length * param.streams > size:
                return (CreateErrors.length_greater_than_size, param.test_number)
            elif (param.special_parameter is not None) and (param.special_parameter < 1):
                return (CreateErrors.special_param_not_in_range, param.test_number)
            elif not control_nist_params_range(param):
                return (CreateErrors.special_param_not_in_range, param.test_number)
    return (CreateErrors.ok, 0)


def control_nist_params_range(param):
    if param.test_number == 1:
        if param.length <= 100:
            return False
    if param.test_number == 2:
        if (param.special_parameter < 20) or (param.special_parameter > int(param.length / 100)):
            return False
    if param.test_number == 3:
        if param.length <= 100:
            return False
    if param.test_number == 4:
        if param.length < 100:
            return False
    if param.test_number == 6:
        if param.length <= 38912:
            return False
    if param.test_number == 7:
        if param.length < 1000:
            return False
    if param.test_number == 8:
        if (param.special_parameter < 2) or (param.special_parameter > 21):
            return False
    if param.test_number == 9:
        if (param.special_parameter < 1) or (param.special_parameter > param.length):
            return False
    if param.test_number == 11:
        if param.special_parameter > (log(param.length, 2) - 6):
            return False
    if (param.test_number == 12) or (param.test_number == 13):
        if param.length < 1000000:
            return False
    if param.test_number == 14:
        if (param.special_parameter < 3) or (param.special_parameter > (log(param.length, 2) - 3)):
            return False
    if param.test_number == 15:
        if (param.length <= 1000000) or (param.special_parameter < 500) or (param.special_parameter > 5000):
            return False
    return True


def fill_array_from_text_input(arr, form, length, streams, test_number, param_name):
    if param_name not in form:
        arr.append(create_nist_param_from_nist_form(test_number, length, streams,
                                                    NistParam.get_default_param_value(test_number)))
        return True
    try:
        params = get_int_array_from_string(form[param_name].value)
    except ValueError:
        return False
    for param in params:
        param_to_append = create_nist_param_from_nist_form(test_number, length, streams, param)
        arr.append(param_to_append)
    return True


def fill_array_from_checkboxes(arr, form, length, streams, test_number, param_name, from_value, to_value):
    j = 0
    for i in range(from_value, to_value):
        param = param_name + str(i)
        if param in form:
            j += 1
            arr.append(create_nist_param_from_nist_form(test_number, length, streams, i))
    if j == 0:
        arr.append(create_nist_param_from_nist_form(test_number, length, streams,
                                                    NistParam.get_default_param_value(test_number)))
