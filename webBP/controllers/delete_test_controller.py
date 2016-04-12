from urllib.parse import urlparse, parse_qs

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
    return
