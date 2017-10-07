import os

from myrequesthandler import MyRequestHandler


def generic_get_js(handler: MyRequestHandler, path_to_js: str):
    handler.send_response(200)
    handler.send_header('Content-type', 'application/javascript')
    handler.end_headers()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    abspath = os.path.join(script_dir, path_to_js)
    with open(abspath, 'rb') as f:
        file_content = f.read()
    handler.wfile.write(file_content)
    return


def get_js_create_tests(handler):
    """
    Returns JavaScript.
    :param handler: MyRequestHandler.
    :return: None
    """
    generic_get_js(handler, '../views/create_tests.js')
    return


def get_js_base_chart(handler: MyRequestHandler):
    generic_get_js(handler, '../views/js/base_chart.js')
    return
