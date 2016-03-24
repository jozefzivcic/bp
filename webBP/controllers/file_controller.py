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
    id = handler.sessions[handler.read_cookie()]
    # handler.file_manager.get_num_of_files_with_name_for_user
    path = join(handler.path_to_users_dir, str(id))
    create_dir_if_not_exists(path)
    path = join(path, handler.parser.get_key('FILES'))
    create_dir_if_not_exists(path)
    file = File()
    file.name = file_name
    file.user_id = id
    file.file_system_path = path
    file.hash = hash_file(file_data)
    handler.file_manager.save_file(file)
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    handler.send_header('Location', '/')
    handler.end_headers()
    path = join(path, str(file.id))
    if file_data:
        with open(path,'wb') as f:
            f.write(file_data)
    return
