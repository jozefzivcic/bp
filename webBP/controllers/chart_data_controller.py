from urllib.parse import urlparse, parse_qs
import json
from myrequesthandler import MyRequestHandler


def get_data_for_base_chart(handler: MyRequestHandler):
    handler.send_response(200)
    handler.send_header('Content-type', 'application/json')
    handler.end_headers()

    data = {}
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)

    if len(queries) != 1 or (queries.get('test_id') is None):
        to_write = json.dumps(data)
        handler.wfile.write(to_write.encode(encoding='utf-8'))
        return

    user_id = handler.sessions[handler.read_cookie()]
    test_id = queries.get('test_id')[0]
    test = handler.test_manager.get_test_for_user_by_id(user_id, test_id)

    if test is None:
        to_write = json.dumps(data)
        handler.wfile.write(to_write.encode(encoding='utf-8'))
        return

    p_values = handler.p_value_provider.get_p_values_for_test(test)
    data['data'] = p_values
    to_write = json.dumps(data)
    handler.wfile.write(to_write.encode(encoding='utf-8'))
    return
