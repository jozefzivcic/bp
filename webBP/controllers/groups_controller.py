import cgi
import io
import os
import re
import zipfile
from os import listdir

from os.path import isfile, join, isdir
from urllib.parse import urlparse, parse_qs

from controllers.common_controller import not_found
from models.group import Group
from helpers import zip_folders, get_param_for_test, set_response_redirect
from models.test import Test


def get_groups(handler):
    """
    Generates page with available groups of tests.
    :param handler: MyRequestHandler.
    :return: None.
    """
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('groups.html')
    user_id = handler.sessions[handler.read_cookie()]
    groups = handler.group_manager.get_groups_for_user(user_id)
    lang = handler.get_user_language(user_id)
    temp_dict = dict(handler.texts[lang])
    temp_dict['vars'] = {}
    temp_dict['vars']['groups'] = groups
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def groups_download_post(handler):
    """
    Function for downloading selected zipped groups of tests.
    :param handler: MyRequestHandler.
    :return: None.
    """
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    user_id = handler.sessions[handler.read_cookie()]
    lang = handler.get_user_language(user_id)
    group_ids = get_group_ids(form)
    ok = False
    try:
        file_object = io.BytesIO()
        zip = zipfile.ZipFile(file_object, 'w', zipfile.ZIP_DEFLATED)
        for group_id in group_ids:
            group = handler.group_manager.get_group_by_id_for_user(group_id, user_id)
            if group.id is None:
                handler.send_response(303)
                handler.send_header('Content-type', 'text/html')
                handler.send_header('Location', '/not_found')
                handler.end_headers()
                return
            for test_id in group.test_id_arr:
                test = handler.test_manager.get_test_for_user_by_id(user_id, test_id)
                directory = handler.results_manager.get_path_for_test(test)
                if directory is not None:
                    test_file = handler.file_manager.get_file_by_id(test.file_id)
                    param = get_param_for_test(handler, test)
                    for base, dirs, files in os.walk(directory):
                        for file in files:
                            file_name = os.path.join(base, file)
                            output_file_name = param.get_output_file_name(test_file.name)
                            output_file_name = '_'.join([output_file_name, file])
                            zip.write(file_name, join('/', output_file_name))
        ok = True
        handler.send_response(200)
        handler.send_header('Content-type', 'application/octet-stream')
        handler.send_header('Content-type', 'application/zip')
        handler.send_header('Content-Disposition', 'attachment; filename="{0}"'.format(handler.texts[lang]['resultszip']))
        handler.end_headers()
    finally:
        zip.close()
        if ok:
            handler.wfile.write(file_object.getvalue())
        file_object.close()
    return


def get_group_ids(form):
    """
    Extracts id's of groups from form.
    :param form: Form from which id's are extracted.
    :return: Array of id's.
    """
    groups = [group for group in form.keys() if group.startswith('group')]
    ids = []
    for group in groups:
        group_id = re.search(r'group([0-9]+)', group).groups()[0]
        ids.append(int(group_id))
    return ids


def get_download_report(handler):
    user_id = handler.sessions[handler.read_cookie()]
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)

    if len(queries) != 1:
        not_found(handler)
        return

    group_id = queries.get('id')[0]
    group = handler.group_manager.get_group_by_id_for_user(group_id, user_id)

    this_dir = os.path.dirname(os.path.realpath(__file__))
    res_dir = join(this_dir, '..', handler.config_storage.path_to_users_dir, str(user_id),
                   handler.config_storage.groups, str(group_id))

    if group is None or (group.total_tests != group.finished_tests) or (not isdir(res_dir)):
        set_response_redirect(handler, '/groups')
        if not isdir(res_dir):
            handler.group_manager.set_statistics_not_computed(group_id)
        return

    ok = False
    files = listdir(res_dir)
    try:
        regex = re.compile(r'^report_for_file_id_(\d+)_and_first_test_id_(\d+).txt$')
        file_object = io.BytesIO()
        zip = zipfile.ZipFile(file_object, 'w', zipfile.ZIP_DEFLATED)
        for file in files:
            file_name = os.path.join(res_dir, file)
            file_id = regex.search(file).groups()[0]
            output_file_name = '{}_f_id_{}.txt'.format(handler.file_manager.get_file_by_id(file_id).name, file_id)
            zip.write(file_name, join('/', output_file_name))
        ok = True
        lang = handler.get_user_language(user_id)
        handler.send_response(200)
        handler.send_header('Content-type', 'application/octet-stream')
        handler.send_header('Content-type', 'application/zip')
        handler.send_header('Content-Disposition',
                            'attachment; filename="{0}"'.format(handler.texts[lang]['summary_report']))
        handler.end_headers()
    finally:
        zip.close()
        if ok:
            handler.wfile.write(file_object.getvalue())
        file_object.close()
    return
