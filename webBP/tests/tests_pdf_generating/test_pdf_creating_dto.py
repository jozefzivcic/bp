from unittest import TestCase

from pdf_generating.pdf_creating_dto import PdfCreatingDto


class TestPdfCreatingDto(TestCase):
    def setUp(self):
        self.creating_dto = PdfCreatingDto()

    def test_has_members(self):
        members = ['template', 'output_file', 'keys_for_template']
        existing = list(vars(self.creating_dto).keys())
        self.assertEqual(sorted(members), sorted(existing))
