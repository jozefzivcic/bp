from unittest import TestCase

from enums.hist_for_tests import HistForTests
from pdf_generating.options.hist_options import HistOptions


class TestHistOptions(TestCase):
    def test_printing(self):
        arr = [HistForTests.ALL_TESTS, HistForTests.INDIVIDUAL_TESTS]
        expected = '<hist_for_tests: "[<HistForTests.ALL_TESTS: 0>, <HistForTests.INDIVIDUAL_TESTS: 1>]">'
        opt = HistOptions(arr)

        ret = str(opt)
        self.assertEqual(expected, ret)

        ret = repr(opt)
        self.assertEqual(expected, ret)

    def test_printing_none(self):
        arr = [None]
        expected = '<hist_for_tests: "[None]">'
        opt = HistOptions(arr)

        ret = str(opt)
        self.assertEqual(expected, ret)
