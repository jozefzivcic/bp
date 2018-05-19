from unittest import TestCase

from pdf_generating.options.file_specification import FileSpecification
from pdf_generating.options.test_file_specification import TestFileSpecification


class TestTestFileSpecification(TestCase):
    def test_printing(self):
        expected = '<tid: "456", file type: "<FileSpecification.RESULTS_FILE: 1>", num: "None">'
        spec = TestFileSpecification(456, FileSpecification.RESULTS_FILE)
        ret = str(spec)
        self.assertEqual(expected, ret)
        ret = repr(spec)
        self.assertEqual(expected, ret)

        expected = '<tid: "654", file type: "<FileSpecification.DATA_FILE: 2>", num: "456">'
        spec = TestFileSpecification(654, FileSpecification.DATA_FILE, 456)
        ret = str(spec)
        self.assertEqual(expected, ret)
        ret = repr(spec)
        self.assertEqual(expected, ret)

    def test_printing_none(self):
        expected = '<tid: "None", file type: "None", num: "None">'
        spec = TestFileSpecification(None, None)
        ret = str(spec)
        self.assertEqual(expected, ret)
        ret = repr(spec)
        self.assertEqual(expected, ret)
