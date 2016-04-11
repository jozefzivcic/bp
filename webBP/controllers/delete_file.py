def delete_file(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('delete_file.html')
    output = template.render(handler.texts['en'])
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def delete_file_post(handler):
    return
