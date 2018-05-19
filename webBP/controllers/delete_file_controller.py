import cgi
import os
from os.path import isfile, isdir, realpath, dirname, abspath, join, exists
from urllib.parse import urlparse, parse_qs

import shutil


def delete_file(handler):
    """
    Generates HTML page for deleting selected file and associated record in database.
    :param handler: MyRequestHandler.
    :return: None.
    """
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)
    error = False
    try:
        file_id = queries.get('id')[0]
        file_id = int(file_id)
    except KeyError:
        error = True
    user_id = handler.sessions[handler.read_cookie()]
    file = handler.file_manager.get_file_by_id(file_id)
    if (file is None) or (file.user_id != user_id) or error:
        handler.send_response(303)
        handler.send_header('Content-type', 'text/html')
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    lang = handler.get_user_language(user_id)
    temp_dict = dict(handler.texts[lang])
    temp_dict['vars'] = {}
    temp_dict['vars']['file'] = file
    template = handler.environment.get_template('delete_file.html')
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def delete_file_post(handler):
    """
    Controls URL query string and if file id belongs to user which sends request, then deletes file with it's record in
    DB.
    :param handler: MyRequestHandler.
    :return: None.
    """
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    file_id = int(form['file_id'].value)
    user_id = handler.sessions[handler.read_cookie()]
    file = handler.file_manager.get_file_by_id(file_id)
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    if file.user_id != user_id:
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return
    tests = handler.test_manager.get_tests_for_file(file)
    num_of_ended_tests = sum(1 for t in tests if t.ended == 1)
    if num_of_ended_tests != len(tests):
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return
    handler.send_header('Location', '/')
    handler.end_headers()
    for test in tests:
        if test.ended:
            path = handler.results_manager.get_path_for_test(test)
            if path is not None:
                handler.results_manager.delete_result(test)
                if isdir(path):
                    shutil.rmtree(path)
        if test.test_table == handler.config_storage.nist:
            handler.nist_manager.delete_nist_param_by_id(test.id)
        group_id = handler.group_manager.get_group_id_by_test(test)
        handler.group_manager.delete_test_from_group(test)
        handler.test_manager.delete_test(test)
        this_dir = dirname(realpath(__file__))
        res_dir = abspath(join(this_dir, '..', handler.config_storage.path_to_users_dir, str(user_id),
                               handler.config_storage.groups, str(group_id)))
        tests_in_group = handler.group_manager.get_tests_for_group(group_id)
        if not tests_in_group:
            if exists(res_dir):
                shutil.rmtree(res_dir)
        elif exists(res_dir) and len([name for name in os.listdir(res_dir) if os.path.isfile(join(res_dir, name))]) > 1:
            prefix = 'report_for_file_id_{}_and_first_test_id_'.format(file.id)
            for f in os.listdir(res_dir):
                file_path = join(res_dir, f)
                if os.path.isfile(file_path) and prefix in f:
                    os.remove(file_path)

    handler.file_manager.delete_file(file)
    if (file.file_system_path is not None) and isfile(file.file_system_path):
        os.remove(file.file_system_path)
    return
