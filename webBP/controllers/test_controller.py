from urllib.parse import urlparse, parse_qs

from helpers import get_param_for_test


def test_controller(handler):
    """
    Generates HTML page for test and it's details.
    :param handler: MyRequestHandler.
    :return: None.
    """
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)
    error = False
    test_id = None
    try:
        test_id = queries.get('id')[0]
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
    file = handler.file_manager.get_file_by_id(test.file_id)
    test_param = get_param_for_test(handler, test)
    lang = handler.get_user_language(user_id)
    temp_dict = dict(handler.texts[lang])
    temp_dict['vars'] = {}
    temp_dict['vars']['test'] = test
    temp_dict['vars']['file'] = file
    temp_dict['vars']['test_param'] = test_param
    temp_dict['vars']['nist'] = handler.config_storage.nist
    template = handler.environment.get_template('test.html')
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return
