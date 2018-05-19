from unittest import TestCase

from enums.filter_uniformity import FilterUniformity
from enums.test_dep_pairs import TestDepPairs
from pdf_generating.options.file_specification import FileSpecification
from pdf_generating.options.test_dependency_options import TestDependencyOptions
from pdf_generating.options.test_file_specification import TestFileSpecification


class TestTestDependencyOptions(TestCase):
    def test_printing(self):
        arr = [TestFileSpecification(1, FileSpecification.RESULTS_FILE),
               TestFileSpecification(2, FileSpecification.DATA_FILE, 5)]
        expected = '<specs: "[<tid: "1", file type: "<FileSpecification.RESULTS_FILE: 1>", num: "None">, ' \
                   '<tid: "2", file type: "<FileSpecification.DATA_FILE: 2>", num: "5">]", ' \
                   'filter unif: "<FilterUniformity.DO_NOT_FILTER: 0>", ' \
                   'test pairs: "<TestDepPairs.ALL_PAIRS: 0>">'
        opt = TestDependencyOptions(arr, FilterUniformity.DO_NOT_FILTER, TestDepPairs.ALL_PAIRS)

        ret = str(opt)
        self.assertEqual(expected, ret)

        ret = repr(opt)
        self.assertEqual(expected, ret)
