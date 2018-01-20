from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree
from unittest.mock import MagicMock

from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage import ChartsStorage
from common.helper_functions import load_texts_for_generator
from pdf_generating.pdf_creating_dto import PdfCreatingDto
from pdf_generating.pdf_generating_dto import PdfGeneratingDto
from pdf_generating.pdf_generating_error import PdfGeneratingError
from pdf_generating.pdf_generator import PdfGenerator
from tests.data_for_tests.common_data import FileIdData
from tests.data_for_tests.common_functions import get_file_by_id

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
        self.texts = load_texts_for_generator(texts_dir)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_create_dto_for_concrete_chart_unsupported_chart(self):
        pdf_generating_dto = PdfGeneratingDto()
        pdf_generating_dto.language = 'en'
        with self.assertRaises(PdfGeneratingError) as context:
            self.pdf_generator.create_dto_for_concrete_chart(-1, pdf_generating_dto)
        self.assertEqual('Unsupported chart type', str(context.exception))


    def test_prepare_pdf_creating_dto(self):
        charts_storage, vars_dict = get_charts_storage_and_dict()
        template = join(templates_dir, 'report_template.tex')
        keys_for_template = self.texts
        keys_for_template['vars'] = vars_dict
        output_filename = 'something.pdf'

        generating_dto = PdfGeneratingDto(0.01, [1, 2, 3], [ChartType.P_VALUES], 'en', output_filename)
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
        expected = {FileIdData.file1_id: {'file_name': file_1_name,
                                          'chart_info': [{'path_to_chart': path,
                                                          'chart_type': ch_type}]
                                          }
                    }
        ret = self.pdf_generator.prepare_dict_from_charts_storage(charts_storage)
        self.assertEqual(expected, ret)

    def test_prepare_dict_from_charts_storage_advanced(self):
        charts_storage, expected = get_charts_storage_and_dict()
        ret = self.pdf_generator.prepare_dict_from_charts_storage(charts_storage)
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


def get_charts_storage_and_dict():
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
    expected = {FileIdData.file1_id: {'file_name': file_1_name,
                                      'chart_info': [{'path_to_chart': path_1, 'chart_type': ch_type},
                                                     {'path_to_chart': path_2, 'chart_type': ch_type}]
                                      },
                FileIdData.file2_id: {'file_name': file_2_name,
                                      'chart_info': [{'path_to_chart': path_3, 'chart_type': ch_type},
                                                     {'path_to_chart': path_4, 'chart_type': ch_type},
                                                     {'path_to_chart': path_5, 'chart_type': ch_type}]
                                      }
                }
    return charts_storage, expected
