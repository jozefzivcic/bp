import os


def get_js_create_tests(handler):
    """
    Returns JavaScript.
    :param handler: MyRequestHandler.
    :return: None
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'application/javascript')
    handler.end_headers()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    abspath = os.path.join(script_dir, '../views/create_tests.js')
    with open(abspath, 'rb') as f:
        file_content = f.read()
    handler.wfile.write(file_content)
    return
