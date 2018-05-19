from unittest import TestCase

from pdf_generating.pdf_generating_dto import PdfGeneratingDto


class TestPdfGeneratingDto(TestCase):
    def test_str(self):
        dto = PdfGeneratingDto(0.057, [1, 2, 3], ['Type1', 'Type2'], 'lang', 'output.pdf', 'h_options', 'test_dep_opts',
                               'ecdf_options', 'bpt options', 'prop options', True)
        expected = '<alpha: "0.057000", test ids: "[1, 2, 3]", chart types: "[\'Type1\', \'Type2\']", ' \
                   'language: "lang", o filename: "output.pdf", hist opt: "\'h_options\'", ' \
                   'td opt: "\'test_dep_opts\'", ecdf opt: "\'ecdf_options\'", bpt opt: "\'bpt options\'", ' \
                   'prop opt: "\'prop options\'", create_report: "True">'
        self.assertEqual(expected, str(dto))
        self.assertEqual(expected, repr(dto))

    def test_str_none(self):
        dto = PdfGeneratingDto(0.123)
        expected = '<alpha: "0.123000", test ids: "None", chart types: "None", ' \
                   'language: "None", o filename: "None", hist opt: "None", td opt: "None", ' \
                   'ecdf opt: "None", bpt opt: "None", prop opt: "None", create_report: "False">'
        self.assertEqual(expected, str(dto))
        self.assertEqual(expected, repr(dto))
