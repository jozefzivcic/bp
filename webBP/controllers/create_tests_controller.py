import cgi
from urllib.parse import urlparse, parse_qs
from models.test import Test
from helpers import parse_nist_form, get_file_ids_from_nist_form, control_nist_forms


def create_tests(handler):
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    user_id = handler.sessions[handler.read_cookie()]
    files = handler.file_manager.get_files_for_user(user_id).values()
    template = handler.environment.get_template('create_tests.html')
    temp_dict = dict(handler.texts['en'])
    temp_dict['vars'] = {}
    temp_dict['vars']['files'] = files
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
    """if ret != (0,0):
        qstr = ''
        if ret[1] == 1:
            qstr += 'l=1'
        if ret[2] == 1:
            qstr += 's=1'
        if ret[3] == 1:
            qstr += 'p=1'
        location = '/create_tests?' + qstr
        handler.send_header('Location', location)
        handler.end_headers()
        return"""

    t = Test()
    t.user_id = user_id
    t.test_table = handler.parser.get_key('NIST')
    for file_id in file_ids:
        t.file_id = file_id
        for nist_param in nist_params:
            handler.test_manager.store_test_with_nist_param(t, nist_param)
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    handler.send_header('Location', '/')
    handler.end_headers()
    return
