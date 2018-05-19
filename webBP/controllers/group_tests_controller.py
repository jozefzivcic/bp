import cgi
import re
from tempfile import mkdtemp
from urllib.parse import urlparse, parse_qs

from shutil import rmtree

from os.path import join

from charts.chart_type import ChartType
from controllers.common_controller import not_found, error_occurred
from enums.filter_uniformity import FilterUniformity
from enums.hist_for_tests import HistForTests
from enums.prop_formula import PropFormula
from enums.test_dep_pairs import TestDepPairs
from helpers import get_params_for_tests, set_response_ok, get_ids_of_elements_starting_with
from myrequesthandler import MyRequestHandler
from pdf_generating.options.boxplot_pt_options import BoxplotPTOptions
from pdf_generating.options.ecdf_options import EcdfOptions
from pdf_generating.options.file_specification import FileSpecification
from pdf_generating.options.hist_options import HistOptions
from pdf_generating.options.prop_options import PropOptions
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
    except (TypeError, KeyError):
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
            handler.logger.log_warning('User: {} PdfGeneratingDto None'.format(user_id))
            return
        handler.logger.log_info('User: {} PdfGeneratingDto: "{}"'.format(user_id, repr(dto)))
        generator = PdfGenerator(handler.pool, handler.config_storage)
        generator.generate_pdf(dto)
        with open(file_name, 'rb') as f:
            content = f.read()
        set_response_ok(handler, 'application/pdf')
        handler.wfile.write(content)
        handler.logger.log_info('User: {}, generating successful'.format(user_id))
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
    if 5 in ids:
        types.append(ChartType.ECDF)
    if 6 in ids:
        types.append(ChartType.BOXPLOT_PT)
    if 7 in ids:
        types.append(ChartType.PROPORTIONS)
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


def create_hist_options(form: cgi.FieldStorage) -> HistOptions:
    arr = []
    value = form.getvalue('ch_hist_all')
    if value is not None:
        arr.append(HistForTests.ALL_TESTS)
    value = form.getvalue('ch_hist_individual')
    if value is not None:
        arr.append(HistForTests.INDIVIDUAL_TESTS)
    if not arr:
        return None
    options = HistOptions(arr)
    return options


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
    value = form.getvalue('optuniformity')
    if value is None:
        return None
    filter_unif_dict = {'do_not_filter_unif': FilterUniformity.DO_NOT_FILTER,
                        'filter_unif': FilterUniformity.REMOVE_UNIFORM,
                        'filter_non_unif': FilterUniformity.REMOVE_NON_UNIFORM}
    filter_unif = filter_unif_dict.get(value)
    if filter_unif is None:
        return None
    value = form.getvalue('optsubtest')
    if value is None:
        return None
    subtests_dict = {'all_pairs': TestDepPairs.ALL_PAIRS, 'skip_pairs': TestDepPairs.SKIP_PAIRS_FROM_SUBTESTS}
    subtests = subtests_dict.get(value)
    if subtests is None:
        return None
    return TestDependencyOptions(arr, filter_unif, subtests)


def create_ecdf_options(test_ids: list, form: cgi.FieldStorage) -> EcdfOptions:
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
    return EcdfOptions(arr)


def create_boxplot_pt_options(test_ids: list, form: cgi.FieldStorage) -> BoxplotPTOptions:
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
    return BoxplotPTOptions([arr])


def create_nist_report(form: cgi.FieldStorage):
    if not 'ch_nist_report' in form:
        return False
    value = form['ch_nist_report'].value
    return value == 'on'


def create_prop_options(form: cgi.FieldStorage) -> PropOptions:
    value = form.getvalue('opt_prop_formula')
    if value is None:
        return None
    formula = {'original': PropFormula.ORIGINAL,
               'improved': PropFormula.IMPROVED}.get(value)
    if formula is None:
        return None
    options = PropOptions(formula)
    return options


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
    create_report = create_nist_report(form)
    if not chart_types and not create_report:
        return None

    hist_options = None
    test_dep_options = None
    ecdf_options = None
    boxplot_pt_options = None
    prop_options = None

    if ChartType.HISTOGRAM in chart_types:
        hist_options = create_hist_options(form)
        if hist_options is None:
            return None
    if ChartType.TESTS_DEPENDENCY in chart_types:
        test_dep_options = create_dep_options(test_ids, form)
        if test_dep_options is None:
            return None
    if ChartType.ECDF in chart_types:
        ecdf_options = create_ecdf_options(test_ids, form)
        if ecdf_options is None:
            return None
    if ChartType.BOXPLOT_PT in chart_types:
        boxplot_pt_options = create_boxplot_pt_options(test_ids, form)
        if boxplot_pt_options is None:
            return None
    if ChartType.PROPORTIONS in chart_types:
        prop_options = create_prop_options(form)
        if prop_options is None:
            return None
    return PdfGeneratingDto(alpha, test_ids, chart_types, language, file_name, hist_options, test_dep_options,
                            ecdf_options, boxplot_pt_options, prop_options, create_report)
