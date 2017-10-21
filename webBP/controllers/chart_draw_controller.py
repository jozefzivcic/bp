from urllib.parse import urlparse, parse_qs

from helpers import set_response_not_found, set_response_ok
from myrequesthandler import MyRequestHandler


def process_test_id(handler: MyRequestHandler):
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)

    if len(queries) != 1 or (queries.get('test_id') is None):
        set_response_not_found(handler)
        return False

    user_id = handler.sessions[handler.read_cookie()]
    test_id = queries.get('test_id')[0]
    test = handler.test_manager.get_test_for_user_by_id(user_id, test_id)

    if test is None:
        set_response_not_found(handler)
        return False

    set_response_ok(handler)
    return True


def render_template(handler: MyRequestHandler, template: str):
    user_id = handler.sessions[handler.read_cookie()]
    template = handler.environment.get_template(template)
    lang = handler.get_user_language(user_id)
    temp_dict = dict(handler.texts[lang])
    temp_dict['vars'] = {}
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))


def draw_base_chart_for_test(handler: MyRequestHandler):
    if not process_test_id(handler):
        return
    render_template(handler, 'charts/base_chart.html')
    return


def draw_barplot_for_test(handler: MyRequestHandler):
    if not process_test_id(handler):
        return
    render_template(handler, 'charts/barplot.html')
    return
