def currently_running(handler):
    """
    Generates HTML page with currently running tests for logged in user.
    :param handler: MyRequestHandler.
    :return: None.
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('currently_running.html')
    user_id = handler.sessions[handler.read_cookie()]
    tests = handler.currently_running_manager.get_running_tests_for_user(user_id)
    files = {}
    for test in tests:
        files[test.file_id] = handler.file_manager.get_file_by_id(test.file_id)
    lang = handler.get_user_language(user_id)
    temp_dict = dict(handler.texts[lang])
    temp_dict['vars'] = {}
    temp_dict['vars']['tests'] = tests
    temp_dict['vars']['files'] = files
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return
