from os import makedirs
from os.path import dirname, abspath, join, exists
from shutil import rmtree
from unittest import TestCase
from unittest.mock import MagicMock

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_error import ChartsError
from charts.charts_storage import ChartsStorage
from common.helper_functions import load_texts_into_config_parsers
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
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        config_storage = MagicMock()
        config_storage.nist = 'nist'
        config_storage.path_to_pdf_texts = 'texts'
        config_storage.path_to_tex_templates = 'templates'
        self.pdf_generator = PdfGenerator(None, config_storage)
        self.pdf_generator.file_dao.get_file_by_id = MagicMock(side_effect=get_file_by_id)
        self.pdf_generator._charts_creator._results_dao.get_paths_for_test_ids = MagicMock(
            side_effect=results_dao_get_paths_for_test_ids)
        self.pdf_generator._charts_creator._tests_dao.get_tests_by_id_list = MagicMock(
            side_effect=db_test_dao_get_tests_by_id_list)
        self.pdf_generator._charts_creator._p_values_creator._extractor._test_dao.get_test_by_id = MagicMock(
            side_effect=db_test_dao_get_test_by_id)
        self.pdf_generator._charts_creator._p_values_creator._extractor._nist_dao.get_nist_param_for_test = MagicMock(
            side_effect=nist_dao_get_nist_param_for_test)
        self.texts = load_texts_into_config_parsers(texts_dir)

        tests = [TestsIdData.test1_id, TestsIdData.test2_id, TestsIdData.test3_id]
        output_filename = join(working_dir, 'output.pdf')
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
        self.assertAlmostEqual(0.48, ret.alpha, places=1E-6)
        self.assertEqual(self.texts['en']['General']['Tests'], ret.x_label)
        self.assertEqual(self.texts['en']['General']['PValue'], ret.y_label)
        self.assertEqual(self.texts['en']['PValuesChart']['PValuesChart'], ret.title)

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

    def test_prepare_dict_from_charts_storage_basic(self):
        path = '/home/something/chart.png'
        chart_info = ChartInfo(path, ChartType.P_VALUES, FileIdData.file1_id)
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

    def test_get_chart_name(self):
        expected = self.texts['en']['PValuesChart']['PValuesChart']
        ret = self.pdf_generator.get_chart_name('en', ChartType.P_VALUES)
        self.assertEqual(expected, ret)

    def get_charts_storage_and_dict(self):
        charts_storage = ChartsStorage()

        path_1 = '/home/something/chart_1.png'
        chart_info = ChartInfo(path_1, ChartType.P_VALUES, FileIdData.file1_id)
        charts_storage.add_chart_info(chart_info)

        path_2 = '/home/something/chart_2.png'
        chart_info = ChartInfo(path_2, ChartType.P_VALUES, FileIdData.file1_id)
        charts_storage.add_chart_info(chart_info)

        path_3 = '/home/something/chart_3.png'
        chart_info = ChartInfo(path_3, ChartType.P_VALUES, FileIdData.file2_id)
        charts_storage.add_chart_info(chart_info)

        path_4 = '/home/something/chart_4.png'
        chart_info = ChartInfo(path_4, ChartType.P_VALUES, FileIdData.file2_id)
        charts_storage.add_chart_info(chart_info)

        path_5 = '/home/something/chart_5.png'
        chart_info = ChartInfo(path_5, ChartType.P_VALUES, FileIdData.file2_id)
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
                                                         {'path_to_chart': path_5, 'chart_type': ch_type,
                                                          'chart_name': chart_name}]
                                          }
                    }
        return charts_storage, expected
