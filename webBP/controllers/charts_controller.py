from myrequesthandler import MyRequestHandler


def get_charts(handler: MyRequestHandler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()

    template = handler.environment.get_template('charts.html')
    user_id = handler.sessions[handler.read_cookie()]
    tests = handler.test_manager.get_tests_for_user(user_id)
    lang = handler.get_user_language(user_id)
    temp_dict = dict(handler.texts[lang])
    temp_dict['vars'] = {}
    temp_dict['vars']['tests'] = tests
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return
