import cgi
from urllib.parse import urlparse

from helpers import hash_password, render_login_template, set_response_redirect
from models.user import User


def login(handler):
    """
    Generates HTML form for logging.
    :param handler: MyRequestHandler.
    :return: None.
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    render_login_template(handler, False, False)
    return


def wrong_user_name(handler):
    """
    Generates HTML form for logging if given username does not exists.
    :param handler: MyRequestHandler.
    :return: None.
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    render_login_template(handler, True, False)
    return


def wrong_password(handler):
    """
    Generates HTML form for logging if user typed wrong password.
    :param handler: MyRequestHandler.
    :return: None.
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    render_login_template(handler, False, True)
    return


def post_login(handler):
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    user_name = form['username'].value
    password = form['password'].value
    users = handler.user_manager.get_users_with_name(user_name)
    if len(users) != 1:
        set_response_redirect(handler, '/wrong_user_name')
        return
    psswd_hash = hash_password(password)
    user = User(user_name, psswd_hash)
    if not handler.user_manager.check_user_password(user):
        set_response_redirect(handler, '/wrong_password')
        return
    referrer = handler.headers.get('Referer')
    parse_result = urlparse(referrer)
    if parse_result.path in ['/login', '/wrong_user_name', '/wrong_password']:
        location = '/'
    else:
        if parse_result.query:
            location = '{}?{}'.format(parse_result.path, parse_result.query)
        else:
            location = '{}'.format(parse_result.path)

    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    handler.send_header('Location', location)
    sid = handler.write_cookie()
    handler.end_headers()
    str_sid = str(sid)
    handler.sessions[str_sid] = users[0].id
    return
