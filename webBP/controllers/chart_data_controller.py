from urllib.parse import urlparse, parse_qs
import json

from helpers import set_response_ok
from myrequesthandler import MyRequestHandler
from nist_statistics.facade.PValueFacade import PValueFacade
from nist_statistics.p_value_provider import PValueProvider


def process_test_id(handler: MyRequestHandler):
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)

    if len(queries) != 1 or (queries.get('test_id') is None):
        to_write = json.dumps({})
        handler.wfile.write(to_write.encode(encoding='utf-8'))
        return None
    return queries.get('test_id')[0]


def get_data_for_base_chart(handler: MyRequestHandler):
    set_response_ok(handler)

    data = {}
    test_id = process_test_id(handler)
    if test_id is None:
        return

    user_id = handler.sessions[handler.read_cookie()]
    test = handler.test_manager.get_test_for_user_by_id(user_id, test_id)

    if test is None:
        to_write = json.dumps(data)
        handler.wfile.write(to_write.encode(encoding='utf-8'))
        return

    p_value_provider = PValueProvider(handler.pool)
    p_values = p_value_provider.get_p_values_with_order_for_test(test)
    data['data'] = p_values
    to_write = json.dumps(data)
    handler.wfile.write(to_write.encode(encoding='utf-8'))
    return


def get_data_for_barplot(handler: MyRequestHandler):
    set_response_ok(handler)

    data = {}
    test_id = process_test_id(handler)
    if test_id is None:
        return

    user_id = handler.sessions[handler.read_cookie()]
    test = handler.test_manager.get_test_for_user_by_id(user_id, test_id)

    if test is None:
        to_write = json.dumps(data)
        handler.wfile.write(to_write.encode(encoding='utf-8'))
        return

    facade = PValueFacade(handler.pool)
    to_write = facade.get_json_p_value_intervals_for_test(test)
    handler.wfile.write(to_write.encode(encoding='utf-8'))
    return
