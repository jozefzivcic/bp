import cgi
from helpers import create_dir_if_not_exists, hash_file
from os.path import join
from models.file import File


def upload_file(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('upload_file.html')
    temp_dict = dict(handler.texts['en'])
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def upload_file_post(handler):
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    file_name = form['file_name'].value
    file_data = form['file'].value
    user_id = handler.sessions[handler.read_cookie()]
    if file_data != b'':
        if file_name == '':
            file_name = form['file'].filename
        path = create_path(handler.path_to_users_dir, user_id, handler.config_storage.files)
        file = File()
        set_file(file, file_name, user_id, path, file_data)
        handler.file_manager.save_file(file)
        path = join(path, str(file.id))
        if file_data:
            with open(path, 'wb') as f:
                f.write(file_data)
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    handler.send_header('Location', '/')
    handler.end_headers()
    return


def create_path(p, user_id, files):
    path = join(p, str(user_id))
    create_dir_if_not_exists(path)
    path = join(path, files)
    create_dir_if_not_exists(path)
    return path


def set_file(file, file_name, user_id, path, file_data):
    file.name = file_name
    file.user_id = user_id
    file.file_system_path = path
    file.hash = hash_file(file_data)