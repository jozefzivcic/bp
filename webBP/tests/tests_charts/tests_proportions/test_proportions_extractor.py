from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from charts.dto.proportions_dto import ProportionsDto
from charts.proportions.data_for_proportions_drawer import DataForProportionsDrawer
from charts.different_num_of_pvals_error import DifferentNumOfPValsError
from charts.proportions.proportions_extractor import ProportionsExtractor
from common.error.diff_pvalues_len_err import DiffPValuesLenErr
from enums.nist_test_type import NistTestType
from enums.prop_formula import PropFormula
from models.test import Test
from models.nistparam import NistParam
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from tests.data_for_tests.common_data import TestsIdData, dict_for_test_13, dict_for_test_14, dict_for_test_41, \
    short_names_dict
from tests.data_for_tests.common_functions import db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test


def mock_get_nist_param(test: Test) -> NistParam:
    nist_param = NistParam()
    nist_param.test_id = test.id
    nist_param.streams = 1101
    return nist_param


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

    @patch('charts.proportions.proportions_extractor.ProportionsExtractor.filter_x_ticks',
           side_effect=lambda p, t: (p, t))
    @patch('charts.proportions.proportions_extractor.ProportionsExtractor.process_p_vals',
           side_effect=lambda a, p, n: (['t1', 't2'], ['value1', 'value2']))
    @patch('charts.proportions.proportions_extractor.ProportionsExtractor.get_interval',
           side_effect=lambda f, a, n: (0.85, 0.9, 0.95))
    @patch('managers.nisttestmanager.NistTestManager.get_nist_param_for_test', side_effect=mock_get_nist_param)
    def test_get_data_from_acc(self, f_get_param, f_get_interval, f_process, f_filter):
        dto_13 = PValuesDto(dict_for_test_13)
        dto_14 = PValuesDto(dict_for_test_14)
        dto_41 = PValuesDto(dict_for_test_41)
        acc = PValuesAccumulator()
        acc.add(TestsIdData.test1_id, dto_13)
        acc.add(TestsIdData.test2_id, dto_14)
        acc.add(TestsIdData.test3_id, dto_41)
        prop_dto = ProportionsDto(0.07, 'title', 'x_label', 'y_label', PropFormula.ORIGINAL)
        ex_data = self.extractor.get_data_from_accumulator(acc, prop_dto)

        self.assertEqual(1, len(ex_data.get_all_data()))
        self.assertEqual(1, f_get_param.call_count)
        calls = [call(PropFormula.ORIGINAL, 0.07, 1101)]
        f_get_interval.assert_has_calls(calls)
        self.assertEqual(1, f_process.call_count)
        calls = [call([0, 1], ['t1', 't2'])]
        f_filter.assert_has_calls(calls)

        data = ex_data.get_all_data()[0][1]  # type: DataForProportionsDrawer
        self.assertEqual(prop_dto.title, data.title)
        self.assertEqual(prop_dto.x_label, data.x_label)
        self.assertEqual(prop_dto.y_label, data.y_label)
        self.assertAlmostEqual(0.65, data.y_lim_low, 6)
        self.assertAlmostEqual(1.0, data.y_lim_high, 6)
        self.assertEqual([0, 1], data.x_ticks_pos)
        self.assertEqual(['t1', 't2'], data.x_ticks_lab)
        self.assertEqual([0, 1], data.x_values)
        self.assertEqual(['value1', 'value2'], data.y_values)
        self.assertAlmostEqual(0.85, data.y_interval_low, 6)
        self.assertAlmostEqual(0.95, data.y_interval_high, 6)
        self.assertAlmostEqual(0.9, data.y_interval_mid, 6)

    @patch('charts.proportions.proportions_extractor.ProportionsExtractor.process_p_vals',
           side_effect=DifferentNumOfPValsError('Number of p_values in file is different than given as'
                                                ' a parameter streams. (9, 10)', 10, 9))
    @patch('charts.proportions.proportions_extractor.ProportionsExtractor.get_interval',
           side_effect=lambda f, a, n: (0.85, 0.9, 0.95))
    @patch('managers.nisttestmanager.NistTestManager.get_nist_param_for_test', side_effect=mock_get_nist_param)
    def test_get_data_from_acc_catch_expection(self, f_get_param, f_get_interval, f_process):
        dto_13 = PValuesDto(dict_for_test_13)
        dto_14 = PValuesDto(dict_for_test_14)
        dto_41 = PValuesDto(dict_for_test_41)
        acc = PValuesAccumulator()
        acc.add(TestsIdData.test1_id, dto_13)
        acc.add(TestsIdData.test2_id, dto_14)
        acc.add(TestsIdData.test3_id, dto_41)
        prop_dto = ProportionsDto(0.07, 'title', 'x_label', 'y_label', PropFormula.ORIGINAL)
        ex_data = self.extractor.get_data_from_accumulator(acc, prop_dto)
        self.assertEqual(0, len(ex_data.get_all_data()))
        errs = ex_data.get_all_errs()
        self.assertEqual(1, len(errs))
        expected = DiffPValuesLenErr(10, 9)
        err = errs[0]
        self.assertEqual(expected, err)

    @patch('charts.proportions.proportions_extractor.ProportionsExtractor.get_test_name',
           side_effect=lambda names, tid, data_num=None: 'tid: {} data: {}'.format(tid, data_num))
    @patch('charts.proportions.proportions_extractor.ProportionsExtractor.get_proportions',
           side_effect=lambda p, a, num: p[0])
    def test_process_pvals(self, f_get_prop, f_get_name):
        dto_13 = PValuesDto(dict_for_test_13)
        dto_14 = PValuesDto(dict_for_test_14)
        dto_41 = PValuesDto(dict_for_test_41)
        acc = PValuesAccumulator()
        acc.add(TestsIdData.test1_id, dto_13)
        acc.add(TestsIdData.test2_id, dto_14)
        acc.add(TestsIdData.test3_id, dto_41)
        prop_dto = ProportionsDto(0.07, 'title', 'x_label', 'y_label', PropFormula.ORIGINAL, short_names_dict)
        num_of_seqcs = 10
        ret_ticks, ret_y_values = self.extractor.process_p_vals(acc, prop_dto, num_of_seqcs)
        exp_x_ticks = ['tid: {} data: None'.format(TestsIdData.test1_id),
                       'tid: {} data: 1'.format(TestsIdData.test2_id),
                       'tid: {} data: 2'.format(TestsIdData.test2_id),
                       'tid: {} data: 1'.format(TestsIdData.test3_id),
                       'tid: {} data: 2'.format(TestsIdData.test3_id)]
        exp_y_values = [0.857153, 0.593063, 0.759852, 0.980129, 0.759325]
        self.assertEqual(exp_x_ticks, ret_ticks)
        for i, p in enumerate(exp_y_values):
            self.assertAlmostEqual(p, ret_y_values[i], 6, msg='Differ at index {}'.format(i))
        calls = [call(dict_for_test_13['results'], 0.07, 10),
                 call(dict_for_test_14['data1'], 0.07, 10),
                 call(dict_for_test_14['data2'], 0.07, 10),
                 call(dict_for_test_41['data1'], 0.07, 10),
                 call(dict_for_test_41['data2'], 0.07, 10)]
        f_get_prop.assert_has_calls(calls)
        calls = [call(short_names_dict, TestsIdData.test1_id), call(short_names_dict, TestsIdData.test2_id, 1),
                 call(short_names_dict, TestsIdData.test2_id, 2), call(short_names_dict, TestsIdData.test3_id, 1),
                 call(short_names_dict, TestsIdData.test3_id, 2)]
        f_get_name.assert_has_calls(calls)

    def test_get_proportions_raises(self):
        with self.assertRaises(DifferentNumOfPValsError) as ex:
            self.extractor.get_proportions([0.456, 0.654], 0.01, 3)
        self.assertEqual('Number of p_values in file is different than given as a parameter streams. (2, 3)',
                         str(ex.exception))
        self.assertEqual(3, ex.exception.expected_len)
        self.assertEqual(2, ex.exception.actual_len)

    def test_get_proportions_all_zeros(self):
        p_values = [0.0] * 100
        ret = self.extractor.get_proportions(p_values, 0.01, 100)
        self.assertEqual(0.0, ret)

    def test_get_proportions(self):
        p_values = [0.0, 0.456, 0.05, 0.01, 0.1, 0.0, 0.98, 1.0, 0.654, 0.04999999]
        ret = self.extractor.get_proportions(p_values, 0.05, 10)
        self.assertAlmostEqual(0.75, ret, 6)

    def test_get_proportions_more_data(self):
        p_values = [
            0.846090, 0.095798, 0.085431, 0.359100, 0.114683, 0.953329, 0.242417, 0.951216, 0.027401, 0.002575,
            0.441195, 0.351895, 0.223889, 0.595314, 0.335057, 0.951216, 0.714655, 0.935908, 0.529885, 0.382954,
            0.564179, 0.380169, 0.342984, 0.371863, 0.454927, 0.579273, 0.874404, 0.166459, 0.132430, 0.035965,
            0.154302, 0.792141, 0.233750, 0.786588, 0.353690, 0.185948, 0.681264, 0.690668, 0.543000, 0.612262,
            0.438268, 0.178090, 0.390421, 0.335934, 0.695335, 0.191527, 0.642806, 0.735254, 0.707350, 0.164762,
            0.983074, 0.125835, 0.659302, 0.855273, 0.010035, 0.631047, 0.130045, 0.932474, 0.789770, 0.801486,
            0.271153, 0.076920, 0.182898, 0.869626, 0.054023, 0.404572, 0.716470, 0.963136, 0.410284, 0.000486,
            0.885304, 0.642806, 0.540982, 0.363636, 0.660266, 0.567201, 0.359100, 0.730829, 0.812851, 0.512759,
            0.892400, 0.502709, 0.230197, 0.907661, 0.488682, 0.058378, 0.842052, 0.228786, 0.367282, 0.094681,
            0.296823, 0.020780, 0.019006, 0.558131, 0.962384, 0.683152, 0.300951, 0.254280, 0.707350, 0.076607
        ]
        ret = self.extractor.get_proportions(p_values, 0.01, 100)
        self.assertAlmostEqual(0.98, ret, 6)

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
            self.extractor.get_test_name(short_names_dict, 456)
        self.assertEqual('Undefined table "test_table" for test_id: 456. Expected "nist" as test table',
                         str(ex.exception))

    @patch('models.nistparam.NistParam.get_test_type', return_value=NistTestType.TEST_FREQUENCY)
    def test_get_test_name_data_none(self, f_get_nistparam):
        expected = 'Frequency ({})'.format(TestsIdData.test1_id)
        ret = self.extractor.get_test_name(short_names_dict, TestsIdData.test1_id)
        self.assertEqual(expected, ret)
        self.assertEqual(1, f_get_nistparam.call_count)

    @patch('models.nistparam.NistParam.get_test_type', return_value=NistTestType.TEST_FREQUENCY)
    def test_get_test_name_data_(self, f_get_nistparam):
        expected = 'Frequency ({}) data 5'.format(TestsIdData.test1_id)
        ret = self.extractor.get_test_name(short_names_dict, TestsIdData.test1_id, 5)
        self.assertEqual(expected, ret)
        self.assertEqual(1, f_get_nistparam.call_count)

    def test_filter_x_ticks(self):
        ticks_pos = [0, 1, 2, 3]
        ticks = ['t1', 't2', 't3', 't4']
        ret_pos, ret_ticks = self.extractor.filter_x_ticks(ticks_pos, ticks)
        self.assertEqual(ticks_pos, ret_pos)
        self.assertEqual(ticks, ret_ticks)
