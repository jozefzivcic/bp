import cgi
import io
import re
import zipfile
from models.group import Group
from helpers import zip_folders
from models.test import Test


def get_groups(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()
    template = handler.environment.get_template('groups.html')
    user_id = handler.sessions[handler.read_cookie()]
    groups = handler.group_manager.get_groups_for_user(user_id)
    temp_dict = dict(handler.texts['en'])
    temp_dict['vars'] = {}
    temp_dict['vars']['groups'] = groups
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))
    return


def groups_download_post(handler):
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'],})
    handler.send_response(200)
    handler.send_header('Content-type', 'application/octet-stream')
    handler.send_header('Content-type', 'application/zip')
    handler.send_header('Content-Disposition', 'attachment; filename="{0}"'.format(handler.texts['en']['resultszip']))
    handler.end_headers()
    user_id = handler.sessions[handler.read_cookie()]
    group_ids = get_group_ids(form)
    dirs_with_results = []
    test = Test()
    ok = False
    try:
        file_object = io.BytesIO()
        zip = zipfile.ZipFile(file_object, 'w', zipfile.ZIP_DEFLATED)
        for group_id in group_ids:
            group = handler.group_manager.get_group_by_id_for_user(group_id, user_id)
            for test_id in group.test_id_arr:
                test.id = test_id
                directory = handler.results_manager.get_path_for_test(test)
                if directory is not None:
                    dirs_with_results.append(directory)
        zip_folders(zip, dirs_with_results)
        ok = True
    finally:
        zip.close()
        if ok:
            handler.wfile.write(file_object.getvalue())
        file_object.close()
    return


def get_group_ids(form):
    groups = [group for group in form.keys() if group.startswith('group')]
    ids = []
    for group in groups:
        group_id = re.search(r'group([0-9]+)', group).groups()[0]
        ids.append(int(group_id))
    return ids
