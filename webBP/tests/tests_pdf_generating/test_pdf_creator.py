from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree
from unittest.mock import patch, MagicMock

from pdf_generating.pdf_creating_dto import PdfCreatingDto
from pdf_generating.pdf_creating_error import PdfCreatingError
from pdf_generating.pdf_creator import PdfCreator

this_dir = dirname(abspath(__file__))
working_dir = abspath(join(this_dir, 'working_dir'))
templates_dir = abspath(join(this_dir, '..', 'sample_files_for_tests', 'tex_templates'))


def func_do_nothing(*args, **kwargs):
    pass


class TestPdfCreator(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.creator = PdfCreator(working_dir)
        output_pdf = join(working_dir, 'created.pdf')
        self.creating_dto = PdfCreatingDto()
        self.creating_dto.template = join(templates_dir, 'simple_template.tex')
        self.creating_dto.output_file = output_pdf
        self.creating_dto.keys_for_template = {'section1': 'This is first section', 'section2': 'Another section'}

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_check_dto_none_template(self):
        dto = PdfCreatingDto()
        dto.template = None
        with self.assertRaises(TypeError) as context:
            self.creator.create_pdf(dto)
        self.assertEqual('Template specified is None', str(context.exception))

    def test_check_dto_non_existing_template(self):
        dto = PdfCreatingDto()
        dto.template = join(templates_dir, 'something_non_existing')
        self.assertFalse(exists(dto.template))

        with self.assertRaises(ValueError) as context:
            self.creator.create_pdf(dto)
        self.assertEqual('Given template (' + dto.template + ') does no exists', str(context.exception))

    def test_check_none_output_file(self):
        dto = PdfCreatingDto()
        dto.template = join(templates_dir, 'simple_template.tex')
        dto.output_file = None
        with self.assertRaises(TypeError) as context:
            self.creator.create_pdf(dto)
        self.assertEqual('Output file is None', str(context.exception))

    def test_check_dto_non_existing_dir_for_output(self):
        dto = PdfCreatingDto()
        dto.template = join(templates_dir, 'simple_template.tex')
        output_dir = join(working_dir, 'something_non_existing')
        dto.output_file = join(output_dir, 'output.pdf')
        self.assertFalse(exists(output_dir))

        with self.assertRaises(ValueError) as context:
            self.creator.create_pdf(dto)
        self.assertEqual('Directory ' + output_dir + ' for output file does not exists', str(context.exception))

    def test_get_output_dir_and_file_without_extension(self):
        exp_dir = '/home/something'
        exp_file = 'pdf_file'
        directory, file = self.creator.get_output_dir_and_file(join(exp_dir, exp_file))
        self.assertEqual(exp_dir, directory)
        self.assertEqual(exp_file, file)

    def test_get_output_dir_and_file_with_pdf_extension(self):
        exp_dir = '/home/something'
        exp_file = 'pdf_file'
        directory, file = self.creator.get_output_dir_and_file(join(exp_dir, exp_file + '.pdf'))
        self.assertEqual(exp_dir, directory)
        self.assertEqual(exp_file, file)

    def test_get_output_dir_and_file_with_another_extension(self):
        exp_dir = '/home/something'
        exp_file = 'pdf_file.txt'
        directory, file = self.creator.get_output_dir_and_file(join(exp_dir, exp_file))
        self.assertEqual(exp_dir, directory)
        self.assertEqual(exp_file, file)

    @patch('subprocess.run')
    def test_create_pdf_wrong_pdflatex_return_value(self, func):
        m = MagicMock()
        m.returncode = -1
        func.return_value = m
        with self.assertRaises(PdfCreatingError) as context:
            self.creator.create_pdf(self.creating_dto)
        self.assertEqual('Failed LaTeX compilation when generating ' + self.creating_dto.output_file,
                         str(context.exception))

    @patch('shutil.copy2', side_effect=func_do_nothing)
    def test_create_pdf_copy_not_working(self, func):
        with self.assertRaises(PdfCreatingError) as context:
            self.creator.create_pdf(self.creating_dto)
        self.assertEqual('An error occurred while copying ' + self.creating_dto.output_file, str(context.exception))

    def test_create_pdf(self):
        self.creator.create_pdf(self.creating_dto)
        self.assertTrue(exists(self.creating_dto.output_file))
