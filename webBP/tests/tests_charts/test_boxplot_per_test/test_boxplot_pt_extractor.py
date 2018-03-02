from unittest import TestCase
from unittest.mock import MagicMock, patch

from charts.boxplot_per_test.boxplot_pt_extractor import BoxplotPTExtractor
from models.test import Test
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from tests.data_for_tests.common_data import TestsIdData, dict_for_test_13, dict_for_test_41
from tests.data_for_tests.common_functions import db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test, \
    func_prepare_acc


class TestBoxplotPTExtractor(TestCase):
    def setUp(self):
        mock = patch('managers.dbtestmanager.DBTestManager.get_test_by_id', side_effect=db_test_dao_get_test_by_id)
        self.addCleanup(mock.stop)
        mock.start()
        mock = patch('managers.nisttestmanager.NistTestManager.get_nist_param_for_test',
                     side_effect=nist_dao_get_nist_param_for_test)
        self.addCleanup(mock.stop)
        mock.start()

        storage = MagicMock(nist='nist')
        self.extractor = BoxplotPTExtractor(None, storage)

    def test_get_name_from_seq_results(self):
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        name = self.extractor.get_name_from_seq(seq)
        expected = 'Frequency'
        self.assertEqual(expected, name)

    def test_get_name_from_seq_data(self):
        seq = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 2)
        name = self.extractor.get_name_from_seq(seq)
        expected = 'Cumulative Sums data 2'
        self.assertEqual(expected, name)

    @patch('managers.dbtestmanager.DBTestManager.get_test_by_id')
    def test_get_name_from_seq_throws(self, method_mock):
        test = Test()
        test.test_table = 'table'
        method_mock.return_value = test
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        with self.assertRaises(RuntimeError) as ex:
            self.extractor.get_name_from_seq(seq)
        self.assertEqual('Unknown test type table', str(ex.exception))

    def test_get_p_values_results(self):
        acc = func_prepare_acc()
        seq = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        expected = dict_for_test_13['results']
        ret = self.extractor.get_p_values(acc, seq)
        self.assertEqual(expected, ret)

    def test_get_p_values_data(self):
        acc = func_prepare_acc()
        seq = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 1)
        expected = dict_for_test_41['data1']
        ret = self.extractor.get_p_values(acc, seq)
        self.assertEqual(expected, ret)

        seq = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2)
        expected = dict_for_test_41['data2']
        ret = self.extractor.get_p_values(acc, seq)
        self.assertEqual(expected, ret)

