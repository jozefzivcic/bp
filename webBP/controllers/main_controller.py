def main_page(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('main.html')
    id = handler.sessions[handler.read_cookie()]
    tests = handler.test_manager.get_tests_for_user(id)
    files = handler.file_manager.get_files_for_user(id)
    temp_dict = dict(handler.texts['en'])
    temp_dict['vars'] = {}
    temp_dict['vars']['tests'] = tests
    temp_dict['vars']['files'] = files
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def logout(handler):
    ckie = handler.read_cookie()
    del handler.sessions[ckie]
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    handler.send_header('Location', '/')
    handler.end_headers()
    return
