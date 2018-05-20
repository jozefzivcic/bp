def main_page(handler):
    """
    Generates main page with tests, files.
    :param handler: MyRequestHandler.
    :return: None.
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('main.html')
    user_id = handler.sessions[handler.read_cookie()]
    tests = handler.test_manager.get_tests_for_user(user_id)
    files = handler.file_manager.get_files_for_user(user_id)
    lang = handler.get_user_language(user_id)
    temp_dict = dict(handler.texts[lang])
    temp_dict['vars'] = {}
    temp_dict['vars']['tests'] = tests
    temp_dict['vars']['files'] = files
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def logout(handler):
    """
    Logs out user who send this request.
    :param handler: MyRequestHandler.
    :return: None.
    """
    ckie = handler.read_cookie()
    handler.remove_from_cookies(ckie)
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    handler.send_header('Location', '/')
    handler.end_headers()
    return
