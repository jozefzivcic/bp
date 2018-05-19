from unittest import TestCase

from pdf_generating.options.ecdf_options import EcdfOptions
from pdf_generating.options.file_specification import FileSpecification
from pdf_generating.options.test_file_specification import TestFileSpecification


class TestEcdfOptions(TestCase):
    def test_printing(self):
        arr = [TestFileSpecification(1, FileSpecification.RESULTS_FILE),
               TestFileSpecification(2, FileSpecification.DATA_FILE, 5)]
        expected = '<specs: "[<tid: "1", file type: "<FileSpecification.RESULTS_FILE: 1>", num: "None">, ' \
                   '<tid: "2", file type: "<FileSpecification.DATA_FILE: 2>", num: "5">]">'
        opt = EcdfOptions(arr)
        ret = str(opt)
        self.assertEqual(expected, ret)

        ret = repr(opt)
        self.assertEqual(expected, ret)
