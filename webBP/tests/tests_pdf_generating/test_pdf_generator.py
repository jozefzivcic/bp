from configparser import ConfigParser
from copy import deepcopy
from os import makedirs
from os.path import dirname, abspath, join, exists
from shutil import rmtree
from unittest import TestCase
from unittest.mock import MagicMock, patch

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_error import ChartsError
from charts.charts_storage import ChartsStorage
from charts.data_source_info import DataSourceInfo
from charts.dto.histogram_dto import HistogramDto
from charts.dto.p_values_chart_dto import PValuesChartDto
from charts.tests_in_chart import TestsInChart
from common.error.test_dep_seq_len_err import TestDepSeqLenErr
from common.helper_functions import load_texts_into_config_parsers
from common.info.test_dep_unif_info import TestDepUnifInfo
from enums.filter_uniformity import FilterUniformity
from enums.test_dep_pairs import TestDepPairs
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from pdf_generating.options.boxplot_pt_options import BoxplotPTOptions
from pdf_generating.options.ecdf_options import EcdfOptions
from pdf_generating.options.file_specification import FileSpecification
from pdf_generating.options.test_dependency_options import TestDependencyOptions
from pdf_generating.options.test_file_specification import TestFileSpecification
from pdf_generating.pdf_creating_dto import PdfCreatingDto
from pdf_generating.pdf_creating_error import PdfCreatingError
from pdf_generating.pdf_generating_dto import PdfGeneratingDto
from pdf_generating.pdf_generating_error import PdfGeneratingError
from pdf_generating.pdf_generator import PdfGenerator
from tests.data_for_tests.common_data import FileIdData, TestsIdData
from tests.data_for_tests.common_functions import get_file_by_id, results_dao_get_paths_for_test_ids, \
    db_test_dao_get_tests_by_id_list, db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test, \
    result_dao_get_path_for_test

this_dir = dirname(abspath(__file__))
working_dir = abspath(join(this_dir, 'working_dir_pdf_generator'))
texts_dir = abspath(join(this_dir, '..', '..', 'pdf_generating', 'texts'))
templates_dir = abspath(join(this_dir, '..', '..', 'pdf_generating', 'templates'))


class TestPdfGenerator(TestCase):
    def mock_func(self, func_name, side_effect):
        patcher = patch(func_name, side_effect=side_effect)
        self.addCleanup(patcher.stop)
        patcher.start()

    def mock(self):
        self.mock_func('managers.dbtestmanager.DBTestManager.get_test_by_id', db_test_dao_get_test_by_id)
        self.mock_func('managers.dbtestmanager.DBTestManager.get_tests_by_id_list',
                       db_test_dao_get_tests_by_id_list)
        self.mock_func('managers.nisttestmanager.NistTestManager.get_nist_param_for_test',
                       nist_dao_get_nist_param_for_test)
        self.mock_func('managers.filemanager.FileManager.get_file_by_id', get_file_by_id)
        self.mock_func('managers.resultsmanager.ResultsManager.get_paths_for_test_ids',
                       results_dao_get_paths_for_test_ids)
        self.mock_func('managers.resultsmanager.ResultsManager.get_path_for_test', result_dao_get_path_for_test)

    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.mock()
        config_storage = MagicMock(nist='nist', path_to_pdf_texts='texts', path_to_tex_templates='templates')
        self.pdf_generator = PdfGenerator(None, config_storage)
        self.texts = load_texts_into_config_parsers(texts_dir)
        output_filename = join(working_dir, 'output.pdf')

        tests = [TestsIdData.test1_id, TestsIdData.test2_id, TestsIdData.test3_id]
        self.dto_for_one_file = PdfGeneratingDto(0.01, tests, [ChartType.P_VALUES], 'en', output_filename)

        tests = [TestsIdData.test1_id, TestsIdData.test2_id, TestsIdData.test3_id, TestsIdData.test4_id,
                 TestsIdData.test5_id]
        self.dto_for_two_files = PdfGeneratingDto(0.01, tests, [ChartType.P_VALUES], 'en', output_filename)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_generate_pdf_with_charts_error(self):
        message = 'Error occured'
        self.pdf_generator._charts_creator.generate_charts = MagicMock(side_effect=ChartsError(message))
        with self.assertRaises(PdfGeneratingError) as context:
            self.pdf_generator.generate_pdf(self.dto_for_one_file)
        self.assertEqual(message, str(context.exception))

    def test_generate_pdf_with_pdf_creating_error(self):
        message = 'Error occured'
        self.pdf_generator._charts_creator.generate_charts = MagicMock(side_effect=PdfCreatingError(message))
        with self.assertRaises(PdfGeneratingError) as context:
            self.pdf_generator.generate_pdf(self.dto_for_one_file)
        self.assertEqual(message, str(context.exception))

    def test_generate_pdf_one_file(self):
        self.pdf_generator.generate_pdf(self.dto_for_one_file)
        self.assertTrue(exists(self.dto_for_one_file.output_filename))

    def test_generate_pdf_two_files(self):
        self.pdf_generator.generate_pdf(self.dto_for_two_files)
        self.assertTrue(exists(self.dto_for_one_file.output_filename))

    def test_generate_pdf_two_files_two_charts(self):
        self.dto_for_two_files.chart_types = [ChartType.P_VALUES, ChartType.HISTOGRAM]
        self.pdf_generator.generate_pdf(self.dto_for_two_files)
        self.assertTrue(exists(self.dto_for_two_files.output_filename))

    def test_generate_pdf_one_file_three_charts(self):
        self.dto_for_one_file.chart_types = [ChartType.P_VALUES, ChartType.P_VALUES_ZOOMED, ChartType.HISTOGRAM]
        self.pdf_generator.generate_pdf(self.dto_for_one_file)
        self.assertTrue(exists(self.dto_for_one_file.output_filename))

    def test_generate_pdf_dependency_charts(self):
        alpha = 0.01
        output_filename = join(working_dir, 'output.pdf')
        tests = [TestsIdData.test1_id, TestsIdData.test2_id]
        chart_types = [ChartType.TESTS_DEPENDENCY]
        language = 'en'
        specs = [TestFileSpecification(TestsIdData.test1_id, FileSpecification.RESULTS_FILE),
                 TestFileSpecification(TestsIdData.test2_id, FileSpecification.DATA_FILE, 1)]
        test_dep_options = TestDependencyOptions(specs, FilterUniformity.REMOVE_NON_UNIFORM, TestDepPairs.ALL_PAIRS)
        pdf_gen_dto = PdfGeneratingDto(alpha, tests, chart_types, language, output_filename, test_dep_options)
        self.pdf_generator.generate_pdf(pdf_gen_dto)
        self.assertTrue(exists(output_filename))

    def test_generate_pdf_four_dependency_charts(self):
        alpha = 0.01
        output_filename = join(working_dir, 'output.pdf')
        tests = [TestsIdData.test1_id, TestsIdData.test2_id, TestsIdData.test3_id, TestsIdData.test4_id,
                 TestsIdData.test5_id]
        chart_types = [ChartType.TESTS_DEPENDENCY]
        language = 'en'
        specs = [TestFileSpecification(TestsIdData.test1_id, FileSpecification.RESULTS_FILE),
                 TestFileSpecification(TestsIdData.test2_id, FileSpecification.DATA_FILE, 1),
                 TestFileSpecification(TestsIdData.test3_id, FileSpecification.DATA_FILE, 2),
                 TestFileSpecification(TestsIdData.test4_id, FileSpecification.RESULTS_FILE),
                 TestFileSpecification(TestsIdData.test5_id, FileSpecification.RESULTS_FILE)]
        test_dep_options = TestDependencyOptions(specs, FilterUniformity.REMOVE_NON_UNIFORM, TestDepPairs.ALL_PAIRS)
        pdf_gen_dto = PdfGeneratingDto(alpha, tests, chart_types, language, output_filename, test_dep_options)
        self.pdf_generator.generate_pdf(pdf_gen_dto)
        self.assertTrue(exists(output_filename))

    def test_generate_dependency_charts_filter_out_sub_tests(self):
        alpha = 0.01
        output_filename = join(working_dir, 'output.pdf')
        tests = [TestsIdData.test1_id, TestsIdData.test2_id, TestsIdData.test3_id, TestsIdData.test4_id,
                 TestsIdData.test5_id]
        chart_types = [ChartType.TESTS_DEPENDENCY]
        language = 'en'
        specs = [TestFileSpecification(TestsIdData.test1_id, FileSpecification.RESULTS_FILE),
                 TestFileSpecification(TestsIdData.test2_id, FileSpecification.DATA_FILE, 1),
                 TestFileSpecification(TestsIdData.test2_id, FileSpecification.DATA_FILE, 2),
                 TestFileSpecification(TestsIdData.test3_id, FileSpecification.DATA_FILE, 1),
                 TestFileSpecification(TestsIdData.test3_id, FileSpecification.DATA_FILE, 2)]
        test_dep_options = TestDependencyOptions(specs, FilterUniformity.DO_NOT_FILTER,
                                                 TestDepPairs.SKIP_PAIRS_FROM_SUBTESTS)
        pdf_gen_dto = PdfGeneratingDto(alpha, tests, chart_types, language, output_filename, test_dep_options)
        self.pdf_generator.generate_pdf(pdf_gen_dto)
        self.assertTrue(exists(output_filename))

    def test_generate_pdf_one_ecdf(self):
        alpha = 0.05
        output_filename = join(working_dir, 'output.pdf')
        tests = [TestsIdData.test1_id, TestsIdData.test2_id, TestsIdData.test3_id, TestsIdData.test4_id,
                 TestsIdData.test5_id]
        chart_types = [ChartType.ECDF]
        language = 'en'
        specs = [TestFileSpecification(TestsIdData.test1_id, FileSpecification.RESULTS_FILE)]
        ecdf_options = EcdfOptions(specs)
        pdf_gen_dto = PdfGeneratingDto(alpha, tests, chart_types, language, output_filename, None, ecdf_options)
        self.pdf_generator.generate_pdf(pdf_gen_dto)
        self.assertTrue(exists(output_filename))

    def test_generate_pdf_five_ecdf(self):
        alpha = 0.05
        output_filename = join(working_dir, 'output.pdf')
        tests = [TestsIdData.test1_id, TestsIdData.test2_id, TestsIdData.test3_id, TestsIdData.test4_id,
                 TestsIdData.test5_id]
        chart_types = [ChartType.ECDF]
        language = 'en'
        specs = [TestFileSpecification(TestsIdData.test1_id, FileSpecification.RESULTS_FILE),
                 TestFileSpecification(TestsIdData.test2_id, FileSpecification.DATA_FILE, 2),
                 TestFileSpecification(TestsIdData.test3_id, FileSpecification.DATA_FILE, 1),
                 TestFileSpecification(TestsIdData.test4_id, FileSpecification.RESULTS_FILE),
                 TestFileSpecification(TestsIdData.test5_id, FileSpecification.RESULTS_FILE)]
        ecdf_options = EcdfOptions(specs)
        pdf_gen_dto = PdfGeneratingDto(alpha, tests, chart_types, language, output_filename, None, ecdf_options)
        self.pdf_generator.generate_pdf(pdf_gen_dto)
        self.assertTrue(exists(output_filename))

    def test_generate_pdf_one_boxplots_chart(self):
        alpha = 0.05
        output_filename = join(working_dir, 'output.pdf')
        tests = [TestsIdData.test1_id, TestsIdData.test2_id, TestsIdData.test3_id, TestsIdData.test4_id,
                 TestsIdData.test5_id]
        chart_types = [ChartType.BOXPLOT_PT]
        language = 'en'
        specs = [[TestFileSpecification(TestsIdData.test1_id, FileSpecification.RESULTS_FILE),
                  TestFileSpecification(TestsIdData.test2_id, FileSpecification.DATA_FILE, 2),
                  TestFileSpecification(TestsIdData.test3_id, FileSpecification.DATA_FILE, 1)]]
        options = BoxplotPTOptions(specs)
        pdf_gen_dto = PdfGeneratingDto(alpha, tests, chart_types, language, output_filename, None, None, options)
        self.pdf_generator.generate_pdf(pdf_gen_dto)
        self.assertTrue(exists(output_filename))

    def test_generate_pdf_three_boxplot_charts(self):
        alpha = 0.05
        output_filename = join(working_dir, 'output.pdf')
        tests = [TestsIdData.test1_id, TestsIdData.test2_id, TestsIdData.test3_id, TestsIdData.test4_id,
                 TestsIdData.test5_id]
        chart_types = [ChartType.BOXPLOT_PT]
        language = 'en'
        specs = [[TestFileSpecification(TestsIdData.test1_id, FileSpecification.RESULTS_FILE)],
                 [TestFileSpecification(TestsIdData.test2_id, FileSpecification.DATA_FILE, 1),
                  TestFileSpecification(TestsIdData.test2_id, FileSpecification.DATA_FILE, 2),
                  TestFileSpecification(TestsIdData.test3_id, FileSpecification.DATA_FILE, 1),
                  TestFileSpecification(TestsIdData.test3_id, FileSpecification.DATA_FILE, 2)],
                 [TestFileSpecification(TestsIdData.test4_id, FileSpecification.RESULTS_FILE),
                  TestFileSpecification(TestsIdData.test5_id, FileSpecification.RESULTS_FILE)]]
        options = BoxplotPTOptions(specs)
        pdf_gen_dto = PdfGeneratingDto(alpha, tests, chart_types, language, output_filename, None, None, options)
        self.pdf_generator.generate_pdf(pdf_gen_dto)
        self.assertTrue(exists(output_filename))

    def test_generate_pdf_nist_reports(self):
        self.dto_for_two_files.create_nist_report = True
        self.pdf_generator.generate_pdf(self.dto_for_two_files)
        self.assertTrue(exists(self.dto_for_one_file.output_filename))

    @patch('charts.charts_creator.ChartsCreator.generate_charts')
    def test_create_pdf_with_infos_and_errors(self, generate_charts):
        storage = ChartsStorage()
        infos = [TestDepUnifInfo(0.456, True), TestDepUnifInfo(0.654, False)]
        storage.add_infos_from_chart(ChartType.TESTS_DEPENDENCY, infos)
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        errors = [TestDepSeqLenErr(seq1, 123, seq2, 124), TestDepSeqLenErr(seq1, 50, seq2, 51)]
        storage.add_errors_from_chart(ChartType.TESTS_DEPENDENCY, errors)
        generate_charts.return_value = storage
        output_file = join(working_dir, 'output.pdf')
        spec1 = TestFileSpecification(TestsIdData.test1_id, FileSpecification.RESULTS_FILE)
        spec2 = TestFileSpecification(TestsIdData.test2_id, FileSpecification.DATA_FILE, 1)
        test_dep_options = TestDependencyOptions([spec1, spec2], FilterUniformity.DO_NOT_FILTER, TestDepPairs.ALL_PAIRS)
        pdf_dto = PdfGeneratingDto(0.01, [TestsIdData.test1_id], [ChartType.TESTS_DEPENDENCY], 'en', output_file,
                                   test_dep_options)
        self.pdf_generator.generate_pdf(pdf_dto)
        self.assertTrue(exists(output_file))

    def test_create_dto_for_concrete_chart_unsupported_chart(self):
        pdf_generating_dto = PdfGeneratingDto()
        pdf_generating_dto.language = 'en'
        with self.assertRaises(PdfGeneratingError) as context:
            self.pdf_generator.create_dto_for_concrete_chart(-1, pdf_generating_dto)
        self.assertEqual('Unsupported chart type', str(context.exception))

    def test_create_dto_for_concrete_chart_p_values_chart(self):
        generating_dto = PdfGeneratingDto()
        generating_dto.alpha = 0.48
        generating_dto.language = 'en'
        ret = self.pdf_generator.create_dto_for_concrete_chart(ChartType.P_VALUES, generating_dto)

        self.assertEqual(list, type(ret))
        self.assertEqual(PValuesChartDto, type(ret[0]))
        self.assertAlmostEqual(0.48, ret[0].alpha, places=1E-6)
        self.assertEqual(self.texts['en']['General']['Tests'], ret[0].x_label)
        self.assertEqual(self.texts['en']['General']['PValue'], ret[0].y_label)
        self.assertEqual(self.texts['en']['PValuesChart']['PValuesChart'], ret[0].title)

    def test_create_dto_for_concrete_chart_histogram(self):
        generating_dto = PdfGeneratingDto()
        generating_dto.language = 'en'
        ret = self.pdf_generator.create_dto_for_concrete_chart(ChartType.HISTOGRAM, generating_dto)

        self.assertEqual(list, type(ret))
        self.assertEqual(HistogramDto, type(ret[0]))
        self.assertEqual(self.texts['en']['Histogram']['Intervals'], ret[0].x_label)
        self.assertEqual(self.texts['en']['Histogram']['NumOfPValues'], ret[0].y_label)
        self.assertEqual(self.texts['en']['Histogram']['Histogram'], ret[0].title)

    def test_prepare_pdf_creating_dto_no_nist_report(self):
        language = 'en'
        package_language = 'english'
        charts_storage, charts_dict = self.get_charts_storage_and_dict()
        template = join(templates_dir, 'report_template.tex')
        keys_for_template = {'texts': self.texts[language], 'vars': {'package_language': package_language,
                                                                     'charts': charts_dict,
                                                                     'nist_report_dict': None}}
        output_filename = 'something.pdf'

        generating_dto = PdfGeneratingDto(0.01, [1, 2, 3], [ChartType.P_VALUES], language, output_filename)
        pdf_creating_dto = self.pdf_generator.prepare_pdf_creating_dto(generating_dto, charts_storage, None)

        self.assertEqual(PdfCreatingDto, type(pdf_creating_dto))
        self.assertEqual(template, pdf_creating_dto.template)
        self.assertEqual(output_filename, pdf_creating_dto.output_file)
        self.assertEqual(keys_for_template, pdf_creating_dto.keys_for_template)

    @patch('pdf_generating.pdf_generator.PdfGenerator.prepare_nist_report_dict', return_value='something')
    def test_prepare_pdf_creating_dto_nist_report(self, f_prepare_nist):
        charts_storage, charts_dict = self.get_charts_storage_and_dict()

        generating_dto = PdfGeneratingDto(language='en')
        stats_dict = {'key1': 'value1', 'key2': 'value2'}
        pdf_creating_dto = self.pdf_generator.prepare_pdf_creating_dto(generating_dto, charts_storage, stats_dict)

        self.assertEqual(PdfCreatingDto, type(pdf_creating_dto))
        self.assertEqual('something', pdf_creating_dto.keys_for_template['vars']['nist_report_dict'])
        f_prepare_nist.assert_called_once_with(deepcopy(stats_dict))

    def test_prepare_dict_from_charts_storage_escape_chars(self):
        chart_info = ChartInfo(None, 'something', ChartType.P_VALUES, FileIdData.file3_id)
        charts_storage = ChartsStorage()
        charts_storage.add_chart_info(chart_info)

        file_name = 'Third\_file'
        ret = self.pdf_generator.prepare_dict_from_charts_storage(charts_storage, 'en')
        ret_file_name = ret['files'][FileIdData.file3_id]['file_name']
        self.assertEqual(file_name, ret_file_name)

    def test_prepare_dict_from_charts_storage_basic(self):
        path = '/home/something/chart.png'
        chart_info = ChartInfo(None, path, ChartType.P_VALUES, FileIdData.file1_id)
        charts_storage = ChartsStorage()
        charts_storage.add_chart_info(chart_info)
        file_1_name = get_file_by_id(FileIdData.file1_id).name
        ch_type = ChartType.P_VALUES.name
        chart_name = self.texts['en']['PValuesChart']['PValuesChart']
        files = {FileIdData.file1_id: {'file_name': file_1_name,
                                       'chart_info': [{'path_to_chart': path,
                                                       'chart_type': ch_type,
                                                       'chart_name': chart_name
                                                       }]
                                       }
                 }
        expected = {'files': files}
        ret = self.pdf_generator.prepare_dict_from_charts_storage(charts_storage, 'en')
        self.assertEqual(expected, ret)

    @patch('pdf_generating.pdf_generator.PdfGenerator.get_chart_name_base')
    def test_prepare_dict_from_charts_storage_infos_and_errors(self, func):
        def f(l, t):
            if t == ChartType.P_VALUES:
                return txt_dict['PValuesChart']['PValuesChart']
            elif t == ChartType.TESTS_DEPENDENCY:
                return 'test dependency'
            elif t == ChartType.HISTOGRAM:
                return 'histogram_chart'
        func.side_effect = f
        txt_dict = {'General': {'Results': 'results', 'Data': 'data', 'TestId': 'test_id'},
                    'PValuesChart': {'PValuesChart': 'p-values chart'},
                    'InfoTemplates': {'TestDepUnifInfoT': '{} True',
                                      'TestDepUnifInfoF': '{} False'},
                    'ErrTemplates': {'TestDepDifferentLen': '{} {} {} {}'}
                    }
        cfg = ConfigParser()
        cfg.read_dict(txt_dict)
        self.pdf_generator._texts = {'en': cfg}

        path = '/home/something/chart.png'
        chart_info = ChartInfo(None, path, ChartType.P_VALUES, FileIdData.file1_id)
        info1 = TestDepUnifInfo(0.456, True)
        info2 = TestDepUnifInfo(0.951, False)
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        err = TestDepSeqLenErr(seq1, 45, seq2, 456)

        charts_storage = ChartsStorage()
        charts_storage.add_chart_info(chart_info)
        charts_storage.add_infos_from_chart(ChartType.TESTS_DEPENDENCY, [info1, info2])
        charts_storage.add_errors_from_chart(ChartType.HISTOGRAM, [err])

        file_1_name = get_file_by_id(FileIdData.file1_id).name
        ch_type = ChartType.P_VALUES.name
        chart_name = txt_dict['PValuesChart']['PValuesChart']
        expected = {'files': {FileIdData.file1_id: {'file_name': file_1_name,
                                                    'chart_info': [{'path_to_chart': path,
                                                                    'chart_type': ch_type,
                                                                    'chart_name': chart_name
                                                                    }]
                                                    }},
                    'infos': {'test dependency': ['0.456 True', '0.951 False']},
                    'errors': {'histogram\\_chart': ['test_id: {} results test_id: {} data 2 45 456'
                                                 .format(TestsIdData.test1_id, TestsIdData.test2_id)]}

                    }
        ret = self.pdf_generator.prepare_dict_from_charts_storage(charts_storage, 'en')
        self.assertEqual(expected, ret)
        self.assertEqual(3, func.call_count)

    def test_prepare_dict_from_charts_storage_advanced(self):
        charts_storage, expected = self.get_charts_storage_and_dict()
        ret = self.pdf_generator.prepare_dict_from_charts_storage(charts_storage, 'en')
        self.assertEqual(expected, ret)

    @patch('pdf_generating.pdf_generator.PdfGenerator.get_chart_name')
    def test_get_chart_dict_info_and_err_none(self, func):
        chart_name = 'chart name'
        func.side_effect = lambda l, ch_info: chart_name
        language = 'language_str'
        ch_info = ChartInfo(None, 'some_path', ChartType.P_VALUES, 456)
        expected = {'path_to_chart': 'some_path',
                    'chart_type': ChartType.P_VALUES.name,
                    'chart_name': chart_name
                    }
        ret = self.pdf_generator.get_chart_dict(language, ch_info)
        self.assertDictEqual(expected, ret)
        func.assert_called_once_with(language, ch_info)

    @patch('pdf_generating.pdf_generator.PdfGenerator.get_chart_name')
    @patch('common.info.test_dep_unif_info.TestDepUnifInfo.get_message')
    def test_get_chart_dict_err_none(self, f_get_msg, f_ch_name):
        chart_name = 'chart name'
        info_message = 'info message'
        language = 'en'

        f_get_msg.side_effect = lambda t: info_message
        f_ch_name.side_effect = lambda l, c: chart_name

        ch_info = ChartInfo(None, 'some_path', ChartType.P_VALUES, 456)
        info = TestDepUnifInfo(0.456, True)
        expected = {'path_to_chart': 'some_path',
                    'chart_type': ChartType.P_VALUES.name,
                    'chart_name': chart_name,
                    'info_msg': info_message
                    }
        ret = self.pdf_generator.get_chart_dict(language, ch_info, info)

        self.assertDictEqual(expected, ret)
        f_ch_name.assert_called_once_with(language, ch_info)
        self.assertEqual(1, f_get_msg.call_count)

    @patch('pdf_generating.pdf_generator.PdfGenerator.get_chart_name')
    @patch('common.error.test_dep_seq_len_err.TestDepSeqLenErr.get_message')
    def test_get_chart_dict_info_none(self, f_get_msg, f_ch_name):
        chart_name = 'chart name'
        err_message = 'error message'
        language = 'en'

        f_get_msg.side_effect = lambda t: err_message
        f_ch_name.side_effect = lambda l, c: chart_name

        ch_info = ChartInfo(None, 'some_path', ChartType.P_VALUES, 456)
        err = TestDepSeqLenErr(None, 456, None, 457)
        expected = {'path_to_chart': 'some_path',
                    'chart_type': ChartType.P_VALUES.name,
                    'chart_name': chart_name,
                    'err_msg': err_message
                    }
        ret = self.pdf_generator.get_chart_dict(language, ch_info, None, err)

        self.assertDictEqual(expected, ret)
        f_ch_name.assert_called_once_with(language, ch_info)
        self.assertEqual(1, f_get_msg.call_count)

    @patch('pdf_generating.pdf_generator.PdfGenerator.get_chart_name')
    @patch('common.error.test_dep_seq_len_err.TestDepSeqLenErr.get_message')
    @patch('common.info.test_dep_unif_info.TestDepUnifInfo.get_message')
    def test_get_chart_dict(self, info_get_msg, err_get_msg, f_ch_name):
        chart_name = 'chart name'
        info_message = 'info message'
        err_message = 'error message'
        language = 'en'

        info_get_msg.side_effect = lambda t: info_message
        err_get_msg.side_effect = lambda t: err_message
        f_ch_name.side_effect = lambda l, c: chart_name

        ch_info = ChartInfo(None, 'some_path', ChartType.P_VALUES, 456)
        info = TestDepUnifInfo(0.456, True)
        err = TestDepSeqLenErr(None, 456, None, 457)
        expected = {'path_to_chart': 'some_path',
                    'chart_type': ChartType.P_VALUES.name,
                    'chart_name': chart_name,
                    'info_msg': info_message,
                    'err_msg': err_message
                    }
        ret = self.pdf_generator.get_chart_dict(language, ch_info, info, err)

        self.assertDictEqual(expected, ret)
        f_ch_name.assert_called_once_with(language, ch_info)
        self.assertEqual(1, info_get_msg.call_count)
        self.assertEqual(1, err_get_msg.call_count)

    def test_get_file_name(self):
        expected = get_file_by_id(FileIdData.file1_id).name
        file_name = self.pdf_generator.get_file_name(FileIdData.file1_id)
        self.assertEqual(expected, file_name)

        expected = get_file_by_id(FileIdData.file2_id).name
        file_name = self.pdf_generator.get_file_name(FileIdData.file2_id)
        self.assertEqual(expected, file_name)

    def test_loaded_texts(self):
        self.assertEqual(self.texts, self.pdf_generator._texts)

    def test_unsupported_language(self):
        dto = PdfGeneratingDto()
        dto.language = 'us'
        with self.assertRaises(PdfGeneratingError) as context:
            self.pdf_generator.generate_pdf(dto)
        self.assertEqual('Unsupported language (\'us\')', str(context.exception))

    def test_unsupported_chart_type(self):
        dto = self.dto_for_one_file
        dto.chart_types = [ChartType.P_VALUES, -5]
        with self.assertRaises(PdfGeneratingError) as context:
            self.pdf_generator.generate_pdf(dto)
        self.assertEqual('Unsupported chart type: (\'-5\')', str(context.exception))

    def test_no_default_param_for_test_dependency(self):
        self.dto_for_one_file.chart_types = [ChartType.TESTS_DEPENDENCY]
        self.dto_for_one_file.test_dependency_options = None
        with self.assertRaises(PdfGeneratingError) as context:
            self.pdf_generator.generate_pdf(self.dto_for_one_file)
        self.assertEqual('No default options for test dependency chart', str(context.exception))

    def test_get_chart_name_undefined_chart(self):
        ch_info = ChartInfo(None, 'something', -5, 5)
        with self.assertRaises(PdfGeneratingError) as context:
            self.pdf_generator.get_chart_name('en', ch_info)
        self.assertEqual('Undefined chart type: -5', str(context.exception))

    def test_get_chart_name_p_values(self):
        ch_info = ChartInfo(None, 'something', ChartType.P_VALUES, 5)
        expected = self.texts['en']['PValuesChart']['PValuesChart']
        ret = self.pdf_generator.get_chart_name('en', ch_info)
        self.assertEqual(expected, ret)

    def test_get_chart_name_p_values_zoomed(self):
        ch_info = ChartInfo(None, 'something', ChartType.P_VALUES_ZOOMED, 5)
        expected = self.texts['en']['PValuesChartZoomed']['PValuesChartZoomed']
        ret = self.pdf_generator.get_chart_name('en', ch_info)
        self.assertEqual(expected, ret)

    def test_get_chart_name_histogram(self):
        ch_info = ChartInfo(None, 'something', ChartType.HISTOGRAM, 5)
        expected = self.texts['en']['Histogram']['HistogramUpperH']
        ret = self.pdf_generator.get_chart_name('en', ch_info)
        self.assertEqual(expected, ret)

    def test_get_chart_name_test_dependency(self):
        ch_info = ChartInfo(None, 'something', ChartType.TESTS_DEPENDENCY, 5)
        expected = self.texts['en']['TestDependency']['Title']
        ret = self.pdf_generator.get_chart_name('en', ch_info)
        self.assertEqual(expected, ret)

    @patch('pdf_generating.pdf_generator.PdfGenerator.get_ecdf_chart_name')
    def test_get_chart_name_ecdf(self, func):
        language = 'en'
        chart_info = ChartInfo(None, 'something', ChartType.ECDF, 4)
        self.pdf_generator.get_chart_name(language, chart_info)
        func.assert_called_once_with(language, chart_info)

    def test_get_ecdf_chart_name_results(self):
        expected = '{} {} Frequency results'.format(self.texts['en']['ECDF']['Title'],
                                                    self.texts['en']['General']['From'])
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, seq)
        chart_info = ChartInfo(ds_info, 'something', ChartType.ECDF, FileIdData.file1_id)
        ret = self.pdf_generator.get_ecdf_chart_name('en', chart_info)
        self.assertEqual(expected, ret)

    def test_get_ecdf_chart_name_data(self):
        expected = '{} {} Cumulative Sums data 2'.format(self.texts['en']['ECDF']['Title'],
                                                         self.texts['en']['General']['From'])
        seq = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, seq)
        chart_info = ChartInfo(ds_info, 'something', ChartType.ECDF, FileIdData.file1_id)
        ret = self.pdf_generator.get_ecdf_chart_name('en', chart_info)
        self.assertEqual(expected, ret)

    def test_get_ecdf_chart_name_unknown_file_type(self):
        seq = PValueSequence(TestsIdData.test2_id, -5, 2)
        ds_info = DataSourceInfo(TestsInChart.SINGLE_TEST, seq)
        chart_info = ChartInfo(ds_info, 'something', ChartType.ECDF, FileIdData.file1_id)
        with self.assertRaises(RuntimeError) as ex:
            self.pdf_generator.get_ecdf_chart_name('en', chart_info)
        self.assertEqual('Unknown file type -5', str(ex.exception))

    @patch('pdf_generating.pdf_generator.PdfGenerator.get_chart_name_base',
           side_effect=lambda l, ctype: 'test dependency' if ctype == ChartType.TESTS_DEPENDENCY else 'p_values')
    def test_add_infos(self, func):
        cfg = ConfigParser()
        language_dict = {'InfoTemplates': {'TestDepUnifInfoT': '{} True',
                                           'TestDepUnifInfoF': '{} False'}}
        cfg.read_dict(language_dict)
        self.pdf_generator._texts = {'en': cfg}
        charts_dict = {}
        storage = ChartsStorage()
        storage.add_infos_from_chart(ChartType.TESTS_DEPENDENCY, [TestDepUnifInfo(0.456, True),
                                                                  TestDepUnifInfo(0.654, False)])
        storage.add_infos_from_chart(ChartType.P_VALUES, [TestDepUnifInfo(0.123, False)])
        expected = {'infos': {'test dependency': ['0.456 True', '0.654 False'],
                              'p\\_values': ['0.123 False']}}
        self.pdf_generator.add_infos('en', charts_dict, storage)
        self.assertDictEqual(expected, charts_dict)
        self.assertEqual(2, func.call_count)

    @patch('pdf_generating.pdf_generator.PdfGenerator.get_chart_name_base',
           side_effect=lambda l, ctype: 'test dependency' if ctype == ChartType.TESTS_DEPENDENCY else 'p_values')
    def test_add_errors(self, func):
        cfg = ConfigParser()
        language_dict = {'General': {'Results': 'results', 'Data': 'data', 'TestId': 'test_id'},
                         'ErrTemplates': {'TestDepDifferentLen': '{} {} {} {}'}}
        cfg.read_dict(language_dict)
        self.pdf_generator._texts = {'en': cfg}
        charts_dict = {}
        storage = ChartsStorage()
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        storage.add_errors_from_chart(ChartType.TESTS_DEPENDENCY, [TestDepSeqLenErr(seq1, 123, seq2, 124),
                                                                   TestDepSeqLenErr(seq1, 125, seq2, 126)])
        storage.add_errors_from_chart(ChartType.P_VALUES, [TestDepSeqLenErr(seq1, 125, seq2, 127)])
        seq_str = 'test_id: {} results test_id: {} data 2 '.format(TestsIdData.test1_id, TestsIdData.test2_id)
        expected = {'errors': {'test dependency': [seq_str + '123 124', seq_str + '125 126'],
                               'p\\_values': [seq_str + '125 127']}}
        self.pdf_generator.add_errors('en', charts_dict, storage)
        self.assertDictEqual(expected, charts_dict)
        self.assertEqual(2, func.call_count)

    def test_do_not_create_nist_report(self):
        pdf_dto = PdfGeneratingDto()
        pdf_dto.create_nist_report = False
        ret = self.pdf_generator.create_nist_report(pdf_dto, working_dir)
        self.assertIsNone(ret)

    @patch('nist_statistics.statistics_creator.StatisticsCreator.create_stats_for_tests_ids', return_value={'key': 'value', 'a': 'b'})
    def test_create_nist_report(self, f_create_stats):
        pdf_dto = PdfGeneratingDto()
        alpha = 456
        test_ids = [4, 5, 789, 987]
        pdf_dto.alpha = alpha
        pdf_dto.test_ids = test_ids
        pdf_dto.create_nist_report = True
        ret = self.pdf_generator.create_nist_report(pdf_dto, working_dir)
        f_create_stats.assert_called_once_with(deepcopy(test_ids), working_dir, alpha)
        exp_dict = {'key': 'value', 'a': 'b'}
        self.assertEqual(exp_dict, ret)

    def test_prepare_nist_report_dict_none_input(self):
        ret = self.pdf_generator.prepare_nist_report_dict(None)
        self.assertIsNone(ret)

    @patch('pdf_generating.pdf_generator.escape_latex_special_chars', side_effect=lambda x: x)
    @patch('managers.filemanager.FileManager.get_file_by_id', side_effect=get_file_by_id)
    def test_prepare_nist_report(self, f_get_file, f_escape):
        file1_id = FileIdData.file1_id
        file1_path = join(working_dir, 'file1')
        file1_content = 'file 1 content'

        file2_id = FileIdData.file2_id
        file2_path = join(working_dir, 'file2')
        file2_content = 'file 2 content'

        with open(file1_path, 'w') as f:
            f.write(file1_content)
        with open(file2_path, 'w') as f:
            f.write(file2_content)

        in_dict = {file1_id: file1_path, file2_id: file2_path}
        expected = {file1_id: {'file_name': 'First file', 'content': file1_content},
                    file2_id: {'file_name': 'Second file', 'content': file2_content}}
        ret = self.pdf_generator.prepare_nist_report_dict(in_dict)
        self.assertEqual(expected, ret)
        self.assertEqual(2, f_escape.call_count)
        self.assertEqual(2, f_get_file.call_count)

    def get_charts_storage_and_dict(self):
        charts_storage = ChartsStorage()

        path_1 = '/home/something/chart_1.png'
        chart_info = ChartInfo(None, path_1, ChartType.P_VALUES, FileIdData.file1_id)
        charts_storage.add_chart_info(chart_info)

        path_2 = '/home/something/chart_2.png'
        chart_info = ChartInfo(None, path_2, ChartType.P_VALUES, FileIdData.file1_id)
        charts_storage.add_chart_info(chart_info)

        path_3 = '/home/something/chart_3.png'
        chart_info = ChartInfo(None, path_3, ChartType.P_VALUES, FileIdData.file2_id)
        charts_storage.add_chart_info(chart_info)

        path_4 = '/home/something/chart_4.png'
        chart_info = ChartInfo(None, path_4, ChartType.P_VALUES, FileIdData.file2_id)
        charts_storage.add_chart_info(chart_info)

        path_5 = '/home/something/chart_5.png'
        ds_info = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (PValueSequence(4, PValuesFileType.DATA, 3),
                                                              PValueSequence(4, PValuesFileType.DATA, 4)))
        chart_info = ChartInfo(ds_info, path_5, ChartType.TESTS_DEPENDENCY, FileIdData.file2_id)
        charts_storage.add_chart_info(chart_info)

        file_1_name = get_file_by_id(FileIdData.file1_id).name
        file_2_name = get_file_by_id(FileIdData.file2_id).name

        ch_type = ChartType.P_VALUES.name
        chart_name = self.texts['en']['PValuesChart']['PValuesChart']
        files = {FileIdData.file1_id: {'file_name': file_1_name,
                                       'chart_info': [{'path_to_chart': path_1, 'chart_type': ch_type,
                                                       'chart_name': chart_name},
                                                      {'path_to_chart': path_2, 'chart_type': ch_type,
                                                       'chart_name': chart_name}]
                                       },
                 FileIdData.file2_id: {'file_name': file_2_name,
                                       'chart_info': [{'path_to_chart': path_3, 'chart_type': ch_type,
                                                       'chart_name': chart_name},
                                                      {'path_to_chart': path_4, 'chart_type': ch_type,
                                                       'chart_name': chart_name},
                                                      {'path_to_chart': path_5, 'chart_type': ChartType
                                                          .TESTS_DEPENDENCY.name,
                                                       'chart_name': 'Dependency of two tests'}]
                                       }
                 }
        expected = {'files': files}
        return charts_storage, expected
