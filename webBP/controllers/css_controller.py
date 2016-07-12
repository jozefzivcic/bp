import os


def get_bootstrap(handler):
    """
    Returns bootstrap css.
    :param handler: MyRequestHandler.
    :return: None
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/css')
    handler.end_headers()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    abspath = os.path.join(script_dir, '../views/bootstrap/css/bootstrap.min.css')
    with open(abspath, 'rb') as f:
        file_content = f.read()
    handler.wfile.write(file_content)
    return


def get_own_styles(handler):
    """
    Returns own css.
    :param handler: MyRequestHandler.
    :return: None
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/css')
    handler.end_headers()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    abspath = os.path.join(script_dir, '../views/styles.css')
    with open(abspath, 'rb') as f:
        file_content = f.read()
    handler.wfile.write(file_content)
    return


def get_index(handler):
    """
    Returns index css.
    :param handler: MyRequestHandler.
    :return: None
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/css')
    handler.end_headers()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    abspath = os.path.join(script_dir, '../views/index.css')
    with open(abspath, 'rb') as f:
        file_content = f.read()
    handler.wfile.write(file_content)
    return
