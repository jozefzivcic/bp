def not_found(handler):
    """
    This method generates page not found, if none of pages fit to URL.
    :param handler: Pointer to MyRequestHandler.
    :return: None.
    """
    handler.send_response(404)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('not_found.html')
    lang = handler.get_user_language(None)
    output = template.render(handler.texts[lang])
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def error_occurred(handler):
    """
    This method generates web page if an error (exception) occurs.
    :param handler: Pointer to MyRequestHandler.
    :return: None.
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('error_occurred.html')
    lang = handler.get_user_language(None)
    output = template.render(handler.texts[lang])
    handler.wfile.write(output.encode(encoding='utf-8'))
    return
