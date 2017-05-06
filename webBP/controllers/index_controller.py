def index_get(handler):
    """
    This method generates index page.
    :param handler: Pointer to MyRequestHandler.
    :return: None.
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('index.html')
    lang = handler.get_user_language(None)
    output = template.render(handler.texts[lang])
    handler.wfile.write(output.encode(encoding='utf-8'))
    return