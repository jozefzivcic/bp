def not_found(handler):
    handler.send_response(404)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('not_found.html')
    output = template.render(handler.texts['en'])
    handler.wfile.write(output.encode(encoding='utf-8'))
    return
