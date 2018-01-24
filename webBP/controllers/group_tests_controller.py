import cgi
import re
from tempfile import mkdtemp
from urllib.parse import urlparse, parse_qs

from shutil import rmtree

from os.path import join

from charts.chart_type import ChartType
from helpers import set_response_not_found, set_response_ok, get_params_for_tests
from myrequesthandler import MyRequestHandler
from pdf_generating.pdf_generating_dto import PdfGeneratingDto
from pdf_generating.pdf_generating_error import PdfGeneratingError
from pdf_generating.pdf_generator import PdfGenerator


def get_tests_in_group(handler: MyRequestHandler):
    parsed_path = urlparse(handler.path)
    queries = parse_qs(parsed_path.query)
    error = False
    group_id = 0
    try:
        group_id = queries.get('gid')[0]
    except KeyError:
        error = True
    if error:
        set_response_not_found(handler)
        return
    user_id = handler.sessions[handler.read_cookie()]
    group = handler.group_manager.get_group_by_id_for_user(group_id, user_id)
    if group is None:
        set_response_not_found(handler)
    else:
        set_response_ok(handler)

    tests = handler.group_manager.get_tests_for_group(group_id)
    params = get_params_for_tests(handler, tests)
    files = handler.file_manager.get_files_for_user(user_id)

    lang = handler.get_user_language(user_id)
    temp_dict = dict(handler.texts[lang])
    temp_dict['vars'] = {}
    temp_dict['vars']['tests'] = tests
    temp_dict['vars']['params'] = params
    temp_dict['vars']['files'] = files

    template = handler.environment.get_template('groups_tests.html')
    output = template.render(temp_dict)
    handler.wfile.write(output.encode(encoding='utf-8'))


def show_pdf_post(handler: MyRequestHandler):
    form = cgi.FieldStorage(fp=handler.rfile, headers=handler.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                'CONTENT_TYPE': handler.headers[
                                                                                    'Content-Type'], })
    user_id = handler.sessions[handler.read_cookie()]
    lang = handler.get_user_language(user_id)
    test_ids = get_test_ids(form)
    if not handler.test_manager.check_test_ids_belong_to_user(test_ids, user_id):
        set_response_not_found(handler)
        return
    directory = mkdtemp()
    try:
        file_name = join(directory, 'output.pdf')
        dto = PdfGeneratingDto(0.01, test_ids, [ChartType.P_VALUES, ChartType.HISTOGRAM], lang, file_name)
        generator = PdfGenerator(handler.pool, handler.config_storage)
        generator.generate_pdf(dto)
        with open(file_name, 'rb') as f:
            content = f.read()
        set_response_ok(handler, 'application/pdf')
        handler.wfile.write(content)
    except PdfGeneratingError:
        set_response_not_found(handler)
    finally:
        rmtree(directory)


def get_test_ids(form):
    """
    Extracts id's of tests from form.
    :param form: Form from which id's are extracted.
    :return: Array of id's.
    """
    tests = [group for group in form.keys() if group.startswith('ch_test_')]
    ids = []
    for test in tests:
        test_id = re.search(r'ch_test_([0-9]+)', test).groups()[0]
        ids.append(int(test_id))
    return ids
