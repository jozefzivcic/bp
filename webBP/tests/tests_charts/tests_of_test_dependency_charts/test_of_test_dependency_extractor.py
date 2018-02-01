from unittest import TestCase
from unittest.mock import MagicMock, patch

from charts.test_dependency.test_dependency_extractor import TestDependencyExtractor
from charts.test_dependency_dto import TestDependencyDto
from models.test import Test
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_accumulator import PValuesAccumulator
from p_value_processing.p_values_dto import PValuesDto
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.sequence_accumulator import SequenceAccumulator
from tests.data_for_tests.common_data import TestsIdData, dict_for_test_13, dict_for_test_14, dict_for_test_41, \
    dict_for_test_42, dict_for_test_43
from tests.data_for_tests.common_functions import db_test_dao_get_test_by_id, nist_dao_get_nist_param_for_test

import common.helper_functions

def func_return_false(p_values1: list, p_values2: list):
    return False


class TestOfTestDependencyExtractor(TestCase):
    def setUp(self):
        self.config_storage = MagicMock()
        self.config_storage.nist = 'nist'
        self.extractor = TestDependencyExtractor(None, self.config_storage)
        self.extractor._test_dao.get_test_by_id = MagicMock(side_effect=db_test_dao_get_test_by_id)
        self.extractor._nist_dao.get_nist_param_for_test = MagicMock(side_effect=nist_dao_get_nist_param_for_test)

        self.p_values_dto_for_test1 = PValuesDto(dict_for_test_13)
        self.p_values_dto_for_test2 = PValuesDto(dict_for_test_14)
        self.p_values_dto_for_test3 = PValuesDto(dict_for_test_41)
        self.p_values_dto_for_test4 = PValuesDto(dict_for_test_42)
        self.p_values_dto_for_test5 = PValuesDto(dict_for_test_43)

        self.p_values_acc = PValuesAccumulator()
        self.p_values_acc.add(TestsIdData.test1_id, self.p_values_dto_for_test1)
        self.p_values_acc.add(TestsIdData.test2_id, self.p_values_dto_for_test2)
        self.p_values_acc.add(TestsIdData.test3_id, self.p_values_dto_for_test3)
        self.p_values_acc.add(TestsIdData.test4_id, self.p_values_dto_for_test4)
        self.p_values_acc.add(TestsIdData.test5_id, self.p_values_dto_for_test5)

    @patch('common.helper_functions.check_for_uniformity')
    def test_get_data_from_accumulator(self, func):
        func.side_effect = func_return_false
        seq_acc = SequenceAccumulator()
        seq_acc.add_sequence(PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS))
        seq_acc.add_sequence(PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS))

        dto = TestDependencyDto(seq_acc, 'Dependency of two tests')
        self.extractor.get_data_from_accumulator(self.p_values_acc, dto)

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
