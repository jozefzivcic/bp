import cgi

import helpers
from models.user import User


def sign_up(handler):
    """
    Generates HTML page for sign up new user.
    :param handler: MyRequestHandler.
    :return: None.
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    helpers.render_signup_template(handler, False, False)
    return


def sign_up_user_exists(handler):
    """
    Generates HTML page for sign up new user if previous attempt with name was unsuccessful, because of existing user
    name.
    :param handler: MyRequestHandler.
    :return: None.
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    helpers.render_signup_template(handler, True, False)
    return


def sign_up_passwords_are_not_the_same(handler):
    """
    Generates HTML page for sign up new user if previous attempt finished with failure, because passwords are not the
    same.
    :param handler: MyRequestHandler.
    :return: None.
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    helpers.render_signup_template(handler, False, True)
    return


def post_sign_up(handler):
    """
    Creates new user and redirect to main page.
    :param handler: MyRequestHandler.
    :return: None.
    """
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    user_name = form['username'].value
    password = form['password'].value
    retype_password = form['retype_password'].value
    users = handler.user_manager.get_users_with_name(user_name)
    if len(users) != 0:
        handler.send_header('Location', '/sign_up_user_exists')
        handler.end_headers()
        return
    if password != retype_password:
        handler.send_header('Location', '/sign_up_passwords_are_not_the_same')
        handler.end_headers()
        return
    hash_password = helpers.hash_password(password)
    user = User(user_name, hash_password)
    handler.user_manager.save_user(user)
    handler.send_header('Location', '/')
    sid = handler.add_new_cookies_for_user(user.id)
    handler.write_cookie(sid)
    handler.end_headers()
    return
