from urllib.parse import urlparse, parse_qs

from nist_statistics.statistics_creator import StatisticsCreator


def compute_stats(handler):
    handler.send_response(303)
    handler.send_header('Content-type', 'text/html')

    user_id = handler.sessions[handler.read_cookie()]
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)

    if len(queries) != 1:
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return

    group_id = queries.get('id')[0]
    group = handler.group_manager.get_group_by_id_for_user(group_id, user_id)

    if group is None or (group.total_tests != group.finished_tests):
        handler.send_header('Location', '/not_found')
        handler.end_headers()
        return

    handler.send_header('Location', '/groups')
    handler.end_headers()
    if group.stats == 1:
        return
    stat_creator = StatisticsCreator(handler.pool, handler.config_storage)
    stat_creator.compute_statistics(group_id, user_id)
    return
