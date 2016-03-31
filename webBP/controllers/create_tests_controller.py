import cgi
from urllib.parse import urlencode
from urllib.parse import urlparse, parse_qs
from models.test import Test
from helpers import parse_nist_form, get_file_ids_from_nist_form, control_nist_forms
from models.nistparam import NistParam


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
    files = handler.file_manager.get_files_for_user(user_id).values()
    template = handler.environment.get_template('create_tests.html')
    temp_dict = dict(handler.texts['en'])
    temp_dict['vars'] = {}
    temp_dict['vars']['files'] = files
    temp_dict['vars']['queries'] = parsed_queries
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def create_tests_post(handler):
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    file_ids = get_file_ids_from_nist_form(form)
    nist_params = parse_nist_form(form)
    user_id = handler.sessions[handler.read_cookie()]
    ret = control_nist_forms(handler, user_id, file_ids, nist_params)
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    if ret != (0, 0):
        qstr = convert_nist_params_to_query(nist_params)
        if ret[0] == 1:
            qstr += '&l=1&t=' + str(ret[1])
        elif ret[0] == 2:
            qstr += '&s=1&t=' + str(ret[1])
        elif ret[0] == 3:
            qstr += '&p=1&t=' + str(ret[1])
        location = '/create_tests?' + qstr
        handler.send_header('Location', location)
        handler.end_headers()
        return

    t = Test()
    t.user_id = user_id
    t.test_table = handler.parser.get_key('NIST')
    for file_id in file_ids:
        t.file_id = file_id
        for nist_param in nist_params:
            handler.test_manager.store_test_with_nist_param(t, nist_param)
    handler.send_header('Location', '/')
    handler.end_headers()
    return


def get_possible_keys_and_values():
    arr = {'l': str, 't': int, 'frequency': int, 'frequency_length': int, 'frequency_streams': int,
           'block_frequency': int, 'block_frequency_length': int, 'block_frequency_streams': int,
           'block_frequency_param': int, 'cumulative_sums': int, 'cumulative_sums_length': int,
           'cumulative_sums_streams': int, 'runs': int, 'runs_length': int, 'runs_streams': int,
           'longest_run_of_ones': int, 'longest_run_of_ones_length': int, 'longest_run_of_ones_streams': int,
           'rank': int, 'rank_length': int, 'rank_streams': int, 'discrete_fourier_transform': int,
           'discrete_fourier_transform_length': int, 'discrete_fourier_transform_streams': int, 'nonperiodic': int,
           'nonperiodic_length': int, 'nonperiodic_streams': int, 'nonperiodic_param': int, 'overlapping': int,
           'overlapping_length': int, 'overlapping_streams': int, 'overlapping_param': int, 'universal': int,
           'universal_length': int, 'universal_streams': int, 'apen': int, 'apen_length': int, 'apen_streams': int,
           'apen_param': int, 'excursion': int, 'excursion_length': int, 'excursion_streams': int, 'excursion_var': int,
           'excursion_var_length': int, 'excursion_var_streams': int, 'serial': int, 'serial_length': int,
           'serial_streams': int, 'serial_param': int, 'linear': int, 'linear_length': int, 'linear_streams': int,
           'linear_param': int}
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
            temp_dict[key] = queries[key][0]
        else:
            return None
    return temp_dict


def convert_nist_params_to_query(params):
    temp_dict = {}
    for param in params:
        cb_name = get_checkbox_name(param.test_number)
        length_name = get_length_name(param.test_number)
        streams_name = get_streams_name(param.test_number)
        param_name = get_param_name(param.test_number)
        temp_dict[cb_name] = 1
        temp_dict[length_name] = param.length
        temp_dict[streams_name] = param.streams
        if param_name is not None:
            temp_dict[param_name] = param.special_parameter
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


def get_length_name(test_number):
    if test_number == 1:
        return 'frequency_length'
    elif test_number == 2:
        return 'block_frequency_length'
    elif test_number == 3:
        return 'cumulative_sums_length'
    elif test_number == 4:
        return 'runs_length'
    elif test_number == 5:
        return 'longest_run_of_ones_length'
    elif test_number == 6:
        return 'rank'
    elif test_number == 7:
        return 'discrete_fourier_transform_length'
    elif test_number == 8:
        return 'nonperiodic_length'
    elif test_number == 9:
        return 'overlapping_length'
    elif test_number == 10:
        return 'universal_length'
    elif test_number == 11:
        return 'apen_length'
    elif test_number == 12:
        return 'excursion_length'
    elif test_number == 13:
        return 'excursion_var_length'
    elif test_number == 14:
        return 'serial_length'
    elif test_number == 15:
        return 'linear_length'
    return None


def get_streams_name(test_number):
    if test_number == 1:
        return 'frequency_streams'
    elif test_number == 2:
        return 'block_frequency_streams'
    elif test_number == 3:
        return 'cumulative_sums_streams'
    elif test_number == 4:
        return 'runs_streams'
    elif test_number == 5:
        return 'longest_run_of_ones_streams'
    elif test_number == 6:
        return 'rank_streams'
    elif test_number == 7:
        return 'discrete_fourier_transform_streams'
    elif test_number == 8:
        return 'nonperiodic_streams'
    elif test_number == 9:
        return 'overlapping_streams'
    elif test_number == 10:
        return 'universal_streams'
    elif test_number == 11:
        return 'apen_streams'
    elif test_number == 12:
        return 'excursion_streams'
    elif test_number == 13:
        return 'excursion_var_streams'
    elif test_number == 14:
        return 'serial_streams'
    elif test_number == 15:
        return 'linear_streams'
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
