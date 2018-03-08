from unittest import TestCase
from unittest.mock import MagicMock, patch

from charts.data_source_info import DataSourceInfo
from charts.dto.test_dependency_dto import TestDependencyDto
from charts.test_dependency.data_for_test_dependency_drawer import DataForTestDependencyDrawer
from charts.test_dependency.test_dependency_extractor import TestDependencyExtractor
from charts.tests_in_chart import TestsInChart
from models.test import Test
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.sequence_accumulator import SequenceAccumulator
from tests.data_for_tests.common_data import TestsIdData, dict_for_test_13, dict_for_test_14, dict_for_test_41, \
    dict_for_test_42, dict_for_test_43
from tests.data_for_tests.common_functions import db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test, \
    func_return_false, func_prepare_acc


class TestOfTestDependencyExtractor(TestCase):
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
        self.extractor = TestDependencyExtractor(None, self.config_storage)
        self.p_values_acc = func_prepare_acc()

    @patch('common.unif_check.check_for_uniformity', side_effect=func_return_false)
    def test_get_data_from_accumulator_ds_info(self, func):
        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS))

        title = 'Dependency of two tests'
        dto = TestDependencyDto(seq_acc, title)
        extracted_data_list = self.extractor.get_data_from_accumulator(self.p_values_acc, dto)
        self.assertEqual(10, len(extracted_data_list))
        self.assertEqual(10, func.call_count)

        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1)
        seq3 = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2)
        seq4 = PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS)
        seq5 = PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS)

        ret = extracted_data_list[0].ds_info
        expected = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq2))
        self.assertEqual(expected, ret)

        ret = extracted_data_list[1].ds_info
        expected = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq3))
        self.assertEqual(expected, ret)

        ret = extracted_data_list[2].ds_info
        expected = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq4))
        self.assertEqual(expected, ret)

        ret = extracted_data_list[3].ds_info
        expected = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq1, seq5))
        self.assertEqual(expected, ret)

        ret = extracted_data_list[4].ds_info
        expected = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq2, seq3))
        self.assertEqual(expected, ret)

        ret = extracted_data_list[5].ds_info
        expected = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq2, seq4))
        self.assertEqual(expected, ret)

        ret = extracted_data_list[6].ds_info
        expected = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq2, seq5))
        self.assertEqual(expected, ret)

        ret = extracted_data_list[7].ds_info
        expected = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq3, seq4))
        self.assertEqual(expected, ret)

        ret = extracted_data_list[8].ds_info
        expected = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq3, seq5))
        self.assertEqual(expected, ret)

        ret = extracted_data_list[9].ds_info
        expected = DataSourceInfo(TestsInChart.PAIR_OF_TESTS, (seq4, seq5))
        self.assertEqual(expected, ret)

    @patch('common.unif_check.check_for_uniformity', side_effect=func_return_false)
    def test_get_data_from_accumulator(self, func):
        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS))

        title = 'Dependency of two tests'
        dto = TestDependencyDto(seq_acc, title)
        extracted_data_list = self.extractor.get_data_from_accumulator(self.p_values_acc, dto)

        self.assertEqual(10, len(extracted_data_list))
        self.assertEqual(10, func.call_count)

        # dependency chart for test1 and test2_data1
        ret_data = extracted_data_list[0].data_for_drawer
        test = db_test_dao_get_test_by_id(TestsIdData.test1_id)
        x_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        test = db_test_dao_get_test_by_id(TestsIdData.test2_id)
        y_label = nist_dao_get_nist_param_for_test(test).get_test_name() + '_data_1'
        data_for_drawer = DataForTestDependencyDrawer(dict_for_test_13['results'], dict_for_test_14['data1'], title,
                                                      x_label, y_label)
        self.compare_data_for_drawer(data_for_drawer, ret_data)

        # dependency chart for test1 and test3_data2
        ret_data = extracted_data_list[1].data_for_drawer
        test = db_test_dao_get_test_by_id(TestsIdData.test1_id)
        x_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        test = db_test_dao_get_test_by_id(TestsIdData.test3_id)
        y_label = nist_dao_get_nist_param_for_test(test).get_test_name() + '_data_2'
        data_for_drawer = DataForTestDependencyDrawer(dict_for_test_13['results'], dict_for_test_41['data2'], title,
                                                      x_label, y_label)
        self.compare_data_for_drawer(data_for_drawer, ret_data)

        # dependency chart for test1 and test4
        ret_data = extracted_data_list[2].data_for_drawer
        test = db_test_dao_get_test_by_id(TestsIdData.test1_id)
        x_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        test = db_test_dao_get_test_by_id(TestsIdData.test4_id)
        y_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        data_for_drawer = DataForTestDependencyDrawer(dict_for_test_13['results'], dict_for_test_42['results'], title,
                                                      x_label, y_label)
        self.compare_data_for_drawer(data_for_drawer, ret_data)

        # dependency chart for test1 and test5
        ret_data = extracted_data_list[3].data_for_drawer
        test = db_test_dao_get_test_by_id(TestsIdData.test1_id)
        x_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        test = db_test_dao_get_test_by_id(TestsIdData.test5_id)
        y_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        data_for_drawer = DataForTestDependencyDrawer(dict_for_test_13['results'], dict_for_test_43['results'], title,
                                                      x_label, y_label)
        self.compare_data_for_drawer(data_for_drawer, ret_data)

        # dependency chart for test2_data1 and test3_data2
        ret_data = extracted_data_list[4].data_for_drawer
        test = db_test_dao_get_test_by_id(TestsIdData.test2_id)
        x_label = nist_dao_get_nist_param_for_test(test).get_test_name() + '_data_1'
        test = db_test_dao_get_test_by_id(TestsIdData.test3_id)
        y_label = nist_dao_get_nist_param_for_test(test).get_test_name() + '_data_2'
        data_for_drawer = DataForTestDependencyDrawer(dict_for_test_14['data1'], dict_for_test_41['data2'], title,
                                                      x_label, y_label)
        self.compare_data_for_drawer(data_for_drawer, ret_data)

        # dependency chart for test2_data1 and test4
        ret_data = extracted_data_list[5].data_for_drawer
        test = db_test_dao_get_test_by_id(TestsIdData.test2_id)
        x_label = nist_dao_get_nist_param_for_test(test).get_test_name() + '_data_1'
        test = db_test_dao_get_test_by_id(TestsIdData.test4_id)
        y_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        data_for_drawer = DataForTestDependencyDrawer(dict_for_test_14['data1'], dict_for_test_42['results'], title,
                                                      x_label, y_label)
        self.compare_data_for_drawer(data_for_drawer, ret_data)

        # dependency chart for test2_data1 and test5
        ret_data = extracted_data_list[6].data_for_drawer
        test = db_test_dao_get_test_by_id(TestsIdData.test2_id)
        x_label = nist_dao_get_nist_param_for_test(test).get_test_name() + '_data_1'
        test = db_test_dao_get_test_by_id(TestsIdData.test5_id)
        y_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        data_for_drawer = DataForTestDependencyDrawer(dict_for_test_14['data1'], dict_for_test_43['results'], title,
                                                      x_label, y_label)
        self.compare_data_for_drawer(data_for_drawer, ret_data)

        # dependency chart for test3_data2 and test4
        ret_data = extracted_data_list[7].data_for_drawer
        test = db_test_dao_get_test_by_id(TestsIdData.test3_id)
        x_label = nist_dao_get_nist_param_for_test(test).get_test_name() + '_data_2'
        test = db_test_dao_get_test_by_id(TestsIdData.test4_id)
        y_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        data_for_drawer = DataForTestDependencyDrawer(dict_for_test_41['data2'], dict_for_test_42['results'], title,
                                                      x_label, y_label)
        self.compare_data_for_drawer(data_for_drawer, ret_data)

        # dependency chart for test3_data2 and test5
        ret_data = extracted_data_list[8].data_for_drawer
        test = db_test_dao_get_test_by_id(TestsIdData.test3_id)
        x_label = nist_dao_get_nist_param_for_test(test).get_test_name() + '_data_2'
        test = db_test_dao_get_test_by_id(TestsIdData.test5_id)
        y_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        data_for_drawer = DataForTestDependencyDrawer(dict_for_test_41['data2'], dict_for_test_43['results'], title,
                                                      x_label, y_label)
        self.compare_data_for_drawer(data_for_drawer, ret_data)

        # dependency chart for test4 and test5
        ret_data = extracted_data_list[9].data_for_drawer
        test = db_test_dao_get_test_by_id(TestsIdData.test4_id)
        x_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        test = db_test_dao_get_test_by_id(TestsIdData.test5_id)
        y_label = nist_dao_get_nist_param_for_test(test).get_test_name()
        data_for_drawer = DataForTestDependencyDrawer(dict_for_test_42['results'], dict_for_test_43['results'], title,
                                                      x_label, y_label)
        self.compare_data_for_drawer(data_for_drawer, ret_data)

    def test_get_test_name_wrong_test_type(self):
        test_table_name = 'another_test_table'

        def dao_side_effect(test_id: int) -> Test:
            test = Test()
            test.id = test_id
            test.test_table = test_table_name
            return test

        self.extractor._test_dao.get_test_by_id = MagicMock(side_effect=dao_side_effect)
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        with self.assertRaises(RuntimeError) as context:
            self.extractor.get_test_name(seq)
        self.assertEqual('Unsupported test type ' + test_table_name, str(context.exception))

    def test_get_test_name_results(self):
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        test = db_test_dao_get_test_by_id(TestsIdData.test1_id)
        expected = nist_dao_get_nist_param_for_test(test).get_test_name()
        ret = self.extractor.get_test_name(seq)
        self.assertEqual(expected, ret)

    def test_get_test_name_data_2(self):
        seq = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        test = db_test_dao_get_test_by_id(TestsIdData.test2_id)
        expected = nist_dao_get_nist_param_for_test(test).get_test_name()
        expected += '_data_2'
        ret = self.extractor.get_test_name(seq)
        self.assertEqual(expected, ret)

    def compare_data_for_drawer(self, expected: DataForTestDependencyDrawer, ret: DataForTestDependencyDrawer):
        self.assertEqual(expected.p_values1, ret.p_values1)
        self.assertEqual(expected.p_values2, ret.p_values2)
        self.assertEqual(expected.title, ret.title)
        self.assertEqual(expected.x_label, ret.x_label)
        self.assertEqual(expected.y_label, ret.y_label)
