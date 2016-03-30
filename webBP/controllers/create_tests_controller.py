import cgi
from urllib.parse import urlparse, parse_qs
from models.test import Test
from helpers import parse_nist_form, get_file_ids_from_nist_form, control_nist_forms
from models.nistparam import NistParam

def create_tests(handler):
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)
    error = False
    err_code = ''
    test_name = ''
    if not (len(queries) == 0 or (len(queries) == 2 and 'e' in queries and 't' in queries)):
        error = True
    if len(queries) == 2:
        err_code = queries.get('e')[0]
        if err_code != 'l' and err_code != 's' and err_code != 'p':
            error = True
        test_num = None
        try:
            test_num = int(queries.get('t')[0])
        except ValueError:
            error = True
        p = NistParam()
        p.test_number = test_num
        test_name = p.get_test_name()
    if error:
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
    temp_dict['vars']['error'] = (err_code, test_name)
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
    if ret != (0,0):
        qstr = ''
        if ret[0] == 1:
            qstr += 'e=l&t=' + str(ret[1])
        elif ret[0] == 2:
            qstr += 'e=s&t=' + str(ret[1])
        elif ret[0] == 3:
            qstr += 'e=p&t=' + str(ret[1])
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
