import cgi
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
        qstr = ''
        if ret[0] == 1:
            qstr += 'l=1&t=' + str(ret[1])
        elif ret[0] == 2:
            qstr += 's=1&t=' + str(ret[1])
        elif ret[0] == 3:
            qstr += 'p=1&t=' + str(ret[1])
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
    arr = {'l': str, 't': int, 'frequency': int, 'frequency_length': int, 'frequency_streams': int, 'block_frequency': int, 'block_frequency_length': int, 'block_frequency_streams': int, 'block_frequency_param': int, 'cumulative_sums': int, 'cumulative_sums_length': int, 'cumulative_sums_streams': int, 'runs': int, 'runs_length': int, 'runs_streams': int, 'longest_run_of_ones': int, 'longest_run_of_ones_length': int, 'longest_run_of_ones_streams': int, 'rank': int, 'rank_length': int, 'rank_streams': int, 'discrete_fourier_transform': int, 'discrete_fourier_transform_length': int, 'discrete_fourier_transform_streams': int, 'nonperiodic': int, 'nonperiodic_length': int, 'nonperiodic_streams': int, 'nonperiodic_param': int, 'overlapping': int, 'overlapping_length': int, 'overlapping_streams': int, 'overlapping_param': int, 'universal': int, 'universal_length': int, 'universal_streams': int, 'apen': int, 'apen_length': int, 'apen_streams': int, 'apen_param': int, 'excursion': int, 'excursion_length': int, 'excursion_streams': int, 'excursion_var': int, 'excursion_var_length': int, 'excursion_var_streams': int, 'serial': int, 'serial_length': int, 'serial_streams': int, 'serial_param': int, 'linear': int, 'linear_length': int, 'linear_streams': int, 'linear_param': int}
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
            except AttributeError:
                return None
        elif isinstance(queries[key][0], possible[key]):
            temp_dict[key] = queries[key][0]
        else:
            return None
    return temp_dict
