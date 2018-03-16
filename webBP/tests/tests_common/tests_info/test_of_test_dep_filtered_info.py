from configparser import ConfigParser
from unittest import TestCase

from common.info.test_dep_filtered_info import TestDepFilteredInfo
from enums.filter_uniformity import FilterUniformity


class TestOfTestDepFilteredInfo(TestCase):
    def test_constructor_throws_greater_than(self):
        with self.assertRaises(ValueError) as ex:
            TestDepFilteredInfo(5, 4, FilterUniformity.REMOVE_UNIFORM)
        self.assertEqual('5 is greater than 4', str(ex.exception))

    def test_constructor_throws_wrong_filter_unif(self):
        with self.assertRaises(ValueError) as ex:
            TestDepFilteredInfo(4, 5, FilterUniformity.DO_NOT_FILTER)
        self.assertEqual('{} not allowed'.format(FilterUniformity.DO_NOT_FILTER), str(ex.exception))

    def test_get_message(self):
        cfg = ConfigParser()
        cfg.read_dict({'InfoTemplates': {'TestDepUnifFiltered': '{} {} unif',
                                         'TestDepNonUnifFiltered': '{} {} non-unif'}})

        info = TestDepFilteredInfo(4, 5, FilterUniformity.REMOVE_UNIFORM)
        message = info.get_message(cfg)
        expected = '4 5 unif'
        self.assertEqual(expected, message)

        info = TestDepFilteredInfo(4, 5, FilterUniformity.REMOVE_NON_UNIFORM)
        message = info.get_message(cfg)
        expected = '4 5 non-unif'
        self.assertEqual(expected, message)
