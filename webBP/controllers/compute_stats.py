from os import makedirs

from os.path import join, exists
from urllib.parse import urlparse, parse_qs

from controllers.common_controller import not_found
from helpers import set_response_redirect
from myrequesthandler import MyRequestHandler
from nist_statistics.statistics_creator import StatisticsCreator


def compute_stats(handler: MyRequestHandler):
    user_id = handler.sessions[handler.read_cookie()]
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)

    if len(queries) != 1:
        not_found(handler)
        return

    group_id = queries.get('id')[0]
    group = handler.group_manager.get_group_by_id_for_user(group_id, user_id)

    if group is None or (group.total_tests != group.finished_tests):
        not_found(handler)
        return

    set_response_redirect(handler, '/groups')
    if group.stats == 1:
        return
    directory = join(handler.config_storage.path_to_users_dir, str(user_id), handler.config_storage.groups,
                     str(group_id))
    if not exists(directory):
        makedirs(directory)
    stat_creator = StatisticsCreator(handler.pool, handler.config_storage)
    stat_creator.compute_statistics(group_id, directory)
    return
