import cgi
import re
from tempfile import mkdtemp
from urllib.parse import urlparse, parse_qs

from shutil import rmtree

from os.path import join

from charts.chart_type import ChartType
from controllers.common_controller import not_found, error_occurred
from helpers import get_params_for_tests, set_response_ok, get_ids_of_elements_starting_with
from myrequesthandler import MyRequestHandler
from pdf_generating.options.file_specification import FileSpecification
from pdf_generating.options.test_dependency_options import TestDependencyOptions
from pdf_generating.options.test_file_specification import TestFileSpecification
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
        not_found(handler)
        return
    user_id = handler.sessions[handler.read_cookie()]
    group = handler.group_manager.get_group_by_id_for_user(group_id, user_id)
    if group is None:
        not_found(handler)
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
        not_found(handler)
        return
    directory = mkdtemp()
    try:
        file_name = join(directory, 'output.pdf')
        dto = get_pdf_generating_dto(form, test_ids, lang, file_name)
        if dto is None:
            not_found(handler)
            return
        generator = PdfGenerator(handler.pool, handler.config_storage)
        generator.generate_pdf(dto)
        with open(file_name, 'rb') as f:
            content = f.read()
        set_response_ok(handler, 'application/pdf')
        handler.wfile.write(content)
    except PdfGeneratingError as ex:
        handler.logger.log_error('Error in show_pdf_post', ex)
        error_occurred(handler)
    finally:
        rmtree(directory)


def get_test_ids(form):
    """
    Extracts id's of tests from form.
    :param form: Form from which id's are extracted.
    :return: Array of id's.
    """
    return get_ids_of_elements_starting_with(form, 'ch_test_')


def get_chart_types(form):
    ids = get_ids_of_elements_starting_with(form, 'ch_chart_type_')
    types = []
    if 1 in ids:
        types.append(ChartType.P_VALUES)
    if 2 in ids:
        types.append(ChartType.P_VALUES_ZOOMED)
    if 3 in ids:
        types.append(ChartType.HISTOGRAM)
    if 4 in ids:
        types.append(ChartType.TESTS_DEPENDENCY)
    return types


def get_alpha(form):
    try:
        alpha_str = form['alpha'].value
    except (KeyError, AttributeError):
        return None
    try:
        alpha = float(alpha_str)
    except ValueError:
        return None
    if alpha > 1.0 or alpha < 0.0:
        return None
    return alpha


def create_dep_options(test_ids, form) -> TestDependencyOptions:
    arr = []
    for test_id in test_ids:
        key = 'num_of_data_for_test_id_' + str(test_id)
        try:
            num_of_data_files = int(form[key].value)
        except ValueError:
            return None
        if num_of_data_files == 0:
            arr.append(TestFileSpecification(test_id, FileSpecification.RESULTS_FILE))
        else:
            for i in range(1, num_of_data_files + 1):
                arr.append(TestFileSpecification(test_id, FileSpecification.DATA_FILE, i))
    return TestDependencyOptions(arr)


def get_pdf_generating_dto(form: cgi.FieldStorage, test_ids: list, language: str, file_name):
    """
    Creates PdfGeneratingDto
    :param form: Submitted form class.
    :param test_ids: Ids of tests for which to create a DTO.
    :param language: User language.
    :param file_name: Output PDF file.
    :return: If some error occurs (invalid forms) then None. PdfCreatingDto otherwise.
    """
    alpha = get_alpha(form)
    if alpha is None:
        return None
    chart_types = get_chart_types(form)
    if not chart_types:
        return None
    test_dep_options = None
    if ChartType.TESTS_DEPENDENCY in chart_types:
        test_dep_options = create_dep_options(test_ids, form)
        if test_dep_options is None:
            return None
    return PdfGeneratingDto(alpha, test_ids, chart_types, language, file_name, test_dep_options)
