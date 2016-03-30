from helpers import parse_nist_form, get_file_ids_from_nist_form, control_forms


def create_tests(handler):
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
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    handler.send_header('Location', '/')
    handler.end_headers()
    file_ids = get_file_ids_from_nist_form(handler)
    my_dict = parse_nist_form(handler)
    control_forms(handler, file_ids, my_dict)
    return
