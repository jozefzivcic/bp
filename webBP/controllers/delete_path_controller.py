import cgi
from urllib.parse import urlparse, parse_qs
from os.path import join
import os


def delete_path(handler):
    """
    Generates HTML page for deleting selected file without deleting associated record in database.
    :param handler: MyRequestHandler.
    :return: None.
    """
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)
    error = False
    try:
        file_id = queries.get('id')[0]
        file_id = int(file_id)
    except KeyError:
        error = True
    user_id = handler.sessions[handler.read_cookie()]
    file = handler.file_manager.get_file_by_id(file_id)
    if (file is None) or (file.user_id != user_id) or error:
        handler.send_response(303)
        handler.send_header('Content-type', 'text/html')
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    temp_dict = dict(handler.texts['en'])
    temp_dict['vars'] = {}
    temp_dict['vars']['file_id'] = file_id
    template = handler.environment.get_template('delete_path.html')
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def delete_path_post(handler):
    """
    Controls URL query string and if file id belongs to user which sends request, then deletes file without deleting
    it's record in DB.
    :param handler: MyRequestHandler.
    :return: None.
    """
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    file_id = int(form['file_id'].value)
    user_id = handler.sessions[handler.read_cookie()]
    file = handler.file_manager.get_file_by_id(file_id)
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    if file.user_id != user_id:
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return
    handler.send_header('Location', '/')
    handler.end_headers()
    handler.file_manager.set_fs_path_to_null(file)
    os.remove(file.file_system_path)
    return
