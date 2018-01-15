from os import makedirs
from os.path import dirname, abspath, join, exists
from unittest import TestCase

from shutil import rmtree

from pdf_generating.pdf_creating_dto import PdfCreatingDto
from pdf_generating.pdf_creator import PdfCreator

this_dir = dirname(abspath(__file__))
working_dir = abspath(join(this_dir, 'working_dir'))
templates_dir = abspath(join(this_dir, '..', 'sample_files_for_tests', 'tex_templates'))


class TestPdfCreator(TestCase):
    def setUp(self):
        if not exists(working_dir):
            makedirs(working_dir)
        self.creator = PdfCreator(working_dir)

    def tearDown(self):
        if exists(working_dir):
            rmtree(working_dir)

    def test_generate_pdf(self):
        output_pdf = join(working_dir, 'generated.pdf')
        dto = PdfCreatingDto()
        dto.template = join(templates_dir, 'simple_template.tex')
        dto.output_file = output_pdf
        dto.keys_for_template = {'section1': 'This is first section', 'section2': 'Another section'}
        self.creator.generate_pdf(dto)
        self.assertTrue(exists(output_pdf))
