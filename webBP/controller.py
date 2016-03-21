import cgi

import helpers
from models.user import User


def login(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    helpers.render_login_template(handler, False, False)
    return


def wrong_user_name(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    helpers.render_login_template(handler, True, False)
    return


def wrong_password(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    helpers.render_login_template(handler, False, True)
    return


def not_found(handler):
    handler.send_response(404)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('not_found.html')
    output = template.render(handler.texts['en'])
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def main_page(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('main.html')
    output = template.render(handler.texts['en'])
    handler.wfile.write(output.encode(encoding='utf-8'))
    return

def post_login(handler):
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD':'POST',
                                                                              'CONTENT_TYPE':handler.headers['Content-Type'],})
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    user_name = form['username'].value
    password = form['password'].value
    num_of_users = handler.user_manager.get_users_with_name(user_name)
    if num_of_users != 1:
        handler.send_header('Location', '/wrong_user_name')
        handler.end_headers()
        return
    hash_password = helpers.hash_password(password)
    user = User(user_name, hash_password)
    if handler.user_manager.check_user_password(user):
        handler.send_header('Location','/')
        sid = handler.write_cookie()
        handler.end_headers()
        str_sid = str(sid)
        handler.sessions[str_sid] = 1
        return
    handler.send_header('Location', '/wrong_password')
    handler.end_headers()
    return

def logout(handler):
    ckie = handler.read_cookie()
    del handler.sessions[ckie]
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    handler.send_header('Location','/')
    handler.end_headers()
    return