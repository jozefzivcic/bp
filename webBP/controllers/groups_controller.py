import cgi
import io
import os
import re
import zipfile
from os import listdir

from os.path import isfile, join

from models.group import Group
from helpers import zip_folders, get_param_for_test
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
    handler.send_response(200)
    handler.send_header('Content-type', 'application/octet-stream')
    handler.send_header('Content-type', 'application/zip')
    handler.send_header('Content-Disposition', 'attachment; filename="{0}"'.format(handler.texts[lang]['resultszip']))
    handler.end_headers()
    group_ids = get_group_ids(form)
    ok = False
    try:
        file_object = io.BytesIO()
        zip = zipfile.ZipFile(file_object, 'w', zipfile.ZIP_DEFLATED)
        for group_id in group_ids:
            group = handler.group_manager.get_group_by_id_for_user(group_id, user_id)
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
