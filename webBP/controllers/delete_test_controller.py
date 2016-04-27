import cgi
from urllib.parse import urlparse, parse_qs
from os.path import isdir
import shutil

from helpers import get_param_for_test


def delete_test(handler):
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)
    error = False
    try:
        test_id = queries.get('id')[0]
        test_id = int(test_id)
    except KeyError:
        error = True
    user_id = handler.sessions[handler.read_cookie()]
    test = handler.test_manager.get_test_for_user_by_id(user_id, test_id)
    if (test is None) or error:
        handler.send_response(303)
        handler.send_header('Content-type', 'text/html')
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    param = get_param_for_test(handler, test)
    temp_dict = dict(handler.texts['en'])
    temp_dict['vars'] = {}
    temp_dict['vars']['test'] = test
    temp_dict['vars']['test_param'] = param
    temp_dict['vars']['file_name'] = handler.file_manager.get_file_by_id(test.file_id).name
    template = handler.environment.get_template('delete_test.html')
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def delete_test_post(handler):
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    test_id = int(form['test_id'].value)
    user_id = handler.sessions[handler.read_cookie()]
    test = handler.test_manager.get_test_for_user_by_id(user_id, test_id)
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    if test is None or test.ended != 1:
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return
    handler.send_header('Location', '/')
    handler.end_headers()
    path = handler.results_manager.get_path_for_test(test)
    handler.results_manager.delete_result(test)
    if (path is not None) and (isdir(path)):
        shutil.rmtree(path)
    if test.test_table == handler.config_storage.nist:
        handler.nist_manager.delete_nist_param_by_id(test.id)
    handler.group_manager.delete_test_from_group(test)
    handler.test_manager.delete_test(test)
    return
