from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree
from unittest.mock import MagicMock

from pdf_generating.pdf_generator import PdfGenerator
from tests.data_for_tests.common_data import FileIdData
from tests.data_for_tests.common_functions import get_file_by_id

this_dir = dirname(abspath(__file__))
working_dir = abspath(join(this_dir, 'working_dir_pdf_generator'))
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

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_get_file_name(self):
        expected = get_file_by_id(FileIdData.file1_id).name
        file_name = self.pdf_generator.get_file_name(FileIdData.file1_id)
        self.assertEqual(expected, file_name)

        expected = get_file_by_id(FileIdData.file2_id).name
        file_name = self.pdf_generator.get_file_name(FileIdData.file2_id)
        self.assertEqual(expected, file_name)
