from urllib.parse import urlparse, parse_qs


def delete_path(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('delete_path.html')
    output = template.render(handler.texts['en'])
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def delete_path_post(handler):
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)
    error = False
    try:
        file_id = queries.get('id')[0]
    except KeyError:
        error = True
    user_id = handler.sessions[handler.read_cookie()]
    file = handler.file_manager.get_file_by_id(file_id)
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')
    if (file.user_id != user_id) or error:
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return
    handler.send_header('Location', '/')
    handler.end_headers()
    handler.file_manager.set_fs_path_to_null(file)
    return
