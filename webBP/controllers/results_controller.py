from urllib.parse import urlparse, parse_qs, quote_plus
from os import listdir
from os.path import isfile, join


def results_controller(handler):
    """
    Generates HTML page with files that represents results of particular test.
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
    id = handler.sessions[handler.read_cookie()]
    test = handler.test_manager.get_test_for_user_by_id(id, test_id)
    if (test == None) or error or len(queries) != 1:
        handler.send_response(303)
        handler.send_header('Content-type', 'text/html')
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    path = handler.results_manager.get_path_for_test(test)
    files = [file for file in listdir(path) if isfile(join(path, file))]
    files.sort()
    ret_files = []
    for file in files:
        ret_files.append((file, quote_plus(file)))
    temp_dict = dict(handler.texts['en'])
    temp_dict['vars'] = {}
    temp_dict['vars']['test_id'] = test_id
    temp_dict['vars']['files'] = ret_files
    template = handler.environment.get_template('results.html')
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def view_file_content(handler):
    """
    Displays content for selected file.
    :param handler: MyRequestHandler.
    :return: None.
    """
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)
    error = False
    test_id = None
    file_name = None
    try:
        test_id = queries.get('id')[0]
        file_name = queries.get('file')[0]
    except KeyError:
        error = True
    id = handler.sessions[handler.read_cookie()]
    test = handler.test_manager.get_test_for_user_by_id(id, test_id)
    if (test == None) or error or len(queries) != 2:
        handler.send_response(303)
        handler.send_header('Content-type', 'text/html')
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    path = handler.results_manager.get_path_for_test(test)
    file = join(path, file_name)
    file_content = None
    with open(file) as f:
        file_content = f.readlines()
    temp_dict = dict(handler.texts['en'])
    temp_dict['vars'] = {}
    temp_dict['vars']['file_content'] = file_content
    template = handler.environment.get_template('file_view.html')
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return
