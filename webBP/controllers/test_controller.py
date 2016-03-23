from urllib.parse import urlparse, parse_qs

from helpers import get_param_for_test


def test_controller(handler):
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)
    error = False
    test_id = None
    try:
        test_id = queries.get('id')[0]
    except KeyError:
        error = True
    id = handler.sessions[handler.read_cookie()]
    test = handler.test_manager.get_test_for_user_by_id(id, test_id)
    if (test == None) or error:
        handler.send_response(404)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        return
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    file = handler.file_manager.get_file_by_id(test.file_id)
    test_param = get_param_for_test(handler, test)
    temp_dict = dict(handler.texts['en'])
    temp_dict['vars'] = {}
    temp_dict['vars']['test'] = test
    temp_dict['vars']['file'] = file
    temp_dict['vars']['test_param'] = test_param
    temp_dict['vars']['nist'] = handler.parser.get_key('NIST')
    template = handler.environment.get_template('test.html')
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return
