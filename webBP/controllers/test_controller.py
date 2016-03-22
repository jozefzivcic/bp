from urllib.parse import urlparse


def test_controller(handler):
    parsed_path = urlparse(handler.path)
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    id = handler.sessions[handler.read_cookie()]
    template = handler.environment.get_template('test.html')
    temp_dict = dict(handler.texts['en'])
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return
