from os.path import dirname, abspath, join
from unittest import TestCase

from p_value_processing.p_values_processing_error import PValuesProcessingError
from p_value_processing.p_values_processor import PValuesProcessor
from p_value_processing.processing_dto import ProcessingDto
from tests.data_for_tests.common_data import dict_for_test_13, dict_for_test_14

this_dir = dirname(abspath(__file__))
sample_files_dir = join(this_dir, '..', 'sample_files_for_tests')


class TestPValuesProcessor(TestCase):
    def setUp(self):
        self.processor = PValuesProcessor()
        self.test1_id = 13
        self.test2_id = 14
        self.dir1 = join(sample_files_dir, 'users', '4', 'tests_results', str(self.test1_id))
        self.dir2 = join(sample_files_dir, 'users', '4', 'tests_results', str(self.test2_id))

    def test_process_None_dirs(self):
        with self.assertRaises(PValuesProcessingError) as context:
            self.processor.process_p_values(None)
        self.assertEqual('No directory for processing', str(context.exception))

    def test_process_zero_dirs(self):
        with self.assertRaises(PValuesProcessingError) as context:
            self.processor.process_p_values(ProcessingDto())
        self.assertEqual('No directory for processing', str(context.exception))

    def test_process_one_dir(self):
        dto = ProcessingDto()
        dto.add(self.test1_id, self.dir1)
        acc = self.processor.process_p_values(dto)
        p_values_dto = acc.get_dto_for_test(self.test1_id)
        self.assertEqual(dict_for_test_13['results'], p_values_dto.get_results_p_values())

    def test_process_two_dirs(self):
        dto = ProcessingDto()
        dto.add(self.test1_id, self.dir1)
        dto.add(self.test2_id, self.dir2)
        acc = self.processor.process_p_values(dto)

        p_values_dto = acc.get_dto_for_test(self.test1_id)
        self.assertEqual(dict_for_test_13['results'], p_values_dto.get_results_p_values())

        p_values_dto = acc.get_dto_for_test(self.test2_id)
        self.assertEqual(dict_for_test_14['results'], p_values_dto.get_results_p_values())
        self.assertEqual(dict_for_test_14['data1'], p_values_dto.get_data_p_values(1))
        self.assertEqual(dict_for_test_14['data2'], p_values_dto.get_data_p_values(2))
