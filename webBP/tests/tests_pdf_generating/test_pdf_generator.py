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
from common.helper_functions import load_texts_into_config_parsers
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
    db_test_dao_get_tests_by_id_list, db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test

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
        test_dep_options = TestDependencyOptions(specs)
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
        test_dep_options = TestDependencyOptions(specs)
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

    def test_prepare_pdf_creating_dto(self):
        language = 'en'
        package_language = 'english'
        charts_storage, charts_dict = self.get_charts_storage_and_dict()
        template = join(templates_dir, 'report_template.tex')
        keys_for_template = {'texts': self.texts[language], 'vars': {'package_language': package_language,
                                                                     'charts': charts_dict}}
        output_filename = 'something.pdf'

        generating_dto = PdfGeneratingDto(0.01, [1, 2, 3], [ChartType.P_VALUES], language, output_filename)
        pdf_creating_dto = self.pdf_generator.prepare_pdf_creating_dto(generating_dto, charts_storage)

        self.assertEqual(PdfCreatingDto, type(pdf_creating_dto))
        self.assertEqual(template, pdf_creating_dto.template)
        self.assertEqual(output_filename, pdf_creating_dto.output_file)
        self.assertEqual(keys_for_template, pdf_creating_dto.keys_for_template)

    def test_prepare_dict_from_charts_storage_escape_chars(self):
        chart_info = ChartInfo(None, 'something', ChartType.P_VALUES, FileIdData.file3_id)
        charts_storage = ChartsStorage()
        charts_storage.add_chart_info(chart_info)

        file_name = 'Third\_file'
        ret = self.pdf_generator.prepare_dict_from_charts_storage(charts_storage, 'en')
        ret_file_name = ret[FileIdData.file3_id]['file_name']
        self.assertEqual(file_name, ret_file_name)

    def test_prepare_dict_from_charts_storage_basic(self):
        path = '/home/something/chart.png'
        chart_info = ChartInfo(None, path, ChartType.P_VALUES, FileIdData.file1_id)
        charts_storage = ChartsStorage()
        charts_storage.add_chart_info(chart_info)
        file_1_name = get_file_by_id(FileIdData.file1_id).name
        ch_type = ChartType.P_VALUES.name
        chart_name = self.texts['en']['PValuesChart']['PValuesChart']
        expected = {FileIdData.file1_id: {'file_name': file_1_name,
                                          'chart_info': [{'path_to_chart': path,
                                                          'chart_type': ch_type,
                                                          'chart_name': chart_name
                                                          }]
                                          }
                    }
        ret = self.pdf_generator.prepare_dict_from_charts_storage(charts_storage, 'en')
        self.assertEqual(expected, ret)

    def test_prepare_dict_from_charts_storage_advanced(self):
        charts_storage, expected = self.get_charts_storage_and_dict()
        ret = self.pdf_generator.prepare_dict_from_charts_storage(charts_storage, 'en')
        self.assertEqual(expected, ret)

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
        expected = {FileIdData.file1_id: {'file_name': file_1_name,
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
        return charts_storage, expected
