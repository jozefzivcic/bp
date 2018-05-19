from unittest import TestCase

from enums.prop_formula import PropFormula
from pdf_generating.options.prop_options import PropOptions


class TestPropOptions(TestCase):
    def test_printing(self):
        opt = PropOptions(PropFormula.ORIGINAL)
        expected = '<formula: "<PropFormula.ORIGINAL: 0>">'

        ret = str(opt)
        self.assertEqual(expected, ret)

        ret = repr(opt)
        self.assertEqual(expected, ret)

        opt = PropOptions(PropFormula.IMPROVED)
        expected = '<formula: "<PropFormula.IMPROVED: 1>">'

        ret = str(opt)
        self.assertEqual(expected, ret)

        ret = repr(opt)
        self.assertEqual(expected, ret)

    def test_printing_none(self):
        opt = PropOptions(None)
        expected = '<formula: "None">'

        ret = str(opt)
        self.assertEqual(expected, ret)

        ret = repr(opt)
        self.assertEqual(expected, ret)
