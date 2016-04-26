def get_groups(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('groups.html')
    user_id = handler.sessions[handler.read_cookie()]
    groups = handler.group_manager.get_groups_for_user(user_id)
    temp_dict = dict(handler.texts['en'])
    temp_dict['vars'] = {}
    temp_dict['vars']['groups'] = groups
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def groups_download_post(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'application/octet-stream')
    handler.send_header('Content-type', 'application/zip')
    handler.send_header('Content-Disposition', 'attachment; filename="file.txt"')
    handler.end_headers()

    handler.wfile.write(b'some data')
    return
