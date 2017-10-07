from urllib.parse import urlparse, parse_qs

from myrequesthandler import MyRequestHandler


def draw_base_chart_for_test(handler: MyRequestHandler):
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)

    if len(queries) != 1 or (queries.get('test_id') is None):
        handler.send_response(303)
        handler.send_header('Content-type', 'text/html')
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return

    user_id = handler.sessions[handler.read_cookie()]
    test_id = queries.get('test_id')[0]
    test = handler.test_manager.get_test_for_user_by_id(user_id, test_id)

    if test is None:
        handler.send_response(303)
        handler.send_header('Content-type', 'text/html')
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return

    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()

    template = handler.environment.get_template('charts/base_chart.html')
    lang = handler.get_user_language(user_id)
    temp_dict = dict(handler.texts[lang])
    temp_dict['vars'] = {}
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return
