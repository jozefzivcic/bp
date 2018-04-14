from unittest import TestCase
from unittest.mock import patch, MagicMock

from charts.proportions.proportions_extractor import ProportionsExtractor
from enums.prop_formula import PropFormula
from models.test import Test
from tests.data_for_tests.common_data import TestsIdData
from tests.data_for_tests.common_functions import db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test


class TestProportionsExtractor(TestCase):
    def mock_func(self, func_name, side_effect):
        patcher = patch(func_name, side_effect=side_effect)
        self.addCleanup(patcher.stop)
        patcher.start()

    def mock(self):
        self.mock_func('managers.dbtestmanager.DBTestManager.get_test_by_id', db_test_dao_get_test_by_id)
        self.mock_func('managers.nisttestmanager.NistTestManager.get_nist_param_for_test',
                       nist_dao_get_nist_param_for_test)

    def setUp(self):
        self.mock()
        self.config_storage = MagicMock(nist='nist')
        self.extractor = ProportionsExtractor(None, self.config_storage)

    def test_get_interval_raises(self):
        with self.assertRaises(RuntimeError) as ex:
            self.extractor.get_interval(2, 0.5, 1000)
        self.assertEqual('Unsupported type of formula: "2"', str(ex.exception))

    def test_get_interval_original(self):
        exp_low = 0.9805607
        exp_mid = 0.99
        exp_high = 0.9994393
        low, mid, high = self.extractor.get_interval(PropFormula.ORIGINAL, 0.01, 1000)
        self.assertAlmostEqual(exp_low, low, 6)
        self.assertAlmostEqual(exp_mid, mid, 6)
        self.assertAlmostEqual(exp_high, high, 6)

        exp_low = 0.9434617
        exp_mid = 0.95
        exp_high = 0.9565383
        low, mid, high = self.extractor.get_interval(PropFormula.ORIGINAL, 0.05, 10000)
        self.assertAlmostEqual(exp_low, low, 6)
        self.assertAlmostEqual(exp_mid, mid, 6)
        self.assertAlmostEqual(exp_high, high, 6)

    def test_get_interval_improved(self):
        exp_low = 0.981819
        exp_mid = 0.99
        exp_high = 0.998181
        low, mid, high = self.extractor.get_interval(PropFormula.IMPROVED, 0.01, 1000)
        self.assertAlmostEqual(exp_low, low, 6)
        self.assertAlmostEqual(exp_mid, mid, 6)
        self.assertAlmostEqual(exp_high, high, 6)

        exp_low = 0.9443334
        exp_mid = 0.95
        exp_high = 0.9556666
        low, mid, high = self.extractor.get_interval(PropFormula.IMPROVED, 0.05, 10000)
        self.assertAlmostEqual(exp_low, low, 6)
        self.assertAlmostEqual(exp_mid, mid, 6)
        self.assertAlmostEqual(exp_high, high, 6)

    @patch('managers.dbtestmanager.DBTestManager.get_test_by_id')
    def test_get_test_name_raises(self, f_get):
        test = Test()
        test.test_table = 'test_table'
        f_get.return_value = test
        with self.assertRaises(RuntimeError) as ex:
            self.extractor.get_test_name(456)
        self.assertEqual('Undefined table "test_table" for test_id: 456. Expected "nist" as test table',
                         str(ex.exception))

    @patch('models.nistparam.NistParam.get_test_name', return_value='Test name')
    def test_get_test_name_data_none(self, f_get_nistparam):
        expected = 'Test name ({})'.format(TestsIdData.test1_id)
        ret = self.extractor.get_test_name(TestsIdData.test1_id)
        self.assertEqual(expected, ret)
        self.assertEqual(1, f_get_nistparam.call_count)

    @patch('models.nistparam.NistParam.get_test_name', return_value='Test name')
    def test_get_test_name_data_(self, f_get_nistparam):
        expected = 'Test name ({}) data 5'.format(TestsIdData.test1_id)
        ret = self.extractor.get_test_name(TestsIdData.test1_id, 5)
        self.assertEqual(expected, ret)
        self.assertEqual(1, f_get_nistparam.call_count)

    def test_filter_x_ticks(self):
        ticks_pos = [0, 1, 2, 3]
        ticks = ['t1', 't2', 't3', 't4']
        ret_pos, ret_ticks = self.extractor.filter_x_ticks(ticks_pos, ticks)
        self.assertEqual(ticks_pos, ret_pos)
        self.assertEqual(ticks, ret_ticks)