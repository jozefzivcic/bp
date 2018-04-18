from configparser import ConfigParser
from unittest.mock import patch, call

from os.path import dirname, abspath, join
from unittest import TestCase

from common.helper_functions import config_parser_to_dict, load_texts_into_dict, load_texts_into_config_parsers, \
    escape_latex_special_chars, convert_specs_to_seq_acc, convert_specs_to_p_value_seq, list_difference, \
    specs_list_to_p_value_seq_list, filter_chart_x_ticks, filter_arr_for_chart_x_axis
from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from pdf_generating.options.file_specification import FileSpecification
from pdf_generating.options.test_file_specification import TestFileSpecification
from tests.data_for_tests.common_data import TestsIdData

this_dir = dirname(abspath(__file__))
sample_texts_dir = join(this_dir, '..', 'sample_files_for_tests', 'sample_texts')


class TestHelperFunctions(TestCase):
    def test_config_parser_to_dict(self):
        expected_dict = {'Section1': {'first': 'first', 'second': 'second'},
                         'Section2': {'third': 'third'},
                         'Section3': {'fourth': 'fourth', 'fifth': 'fifth', 'key': 'key', 'value': 'value'}
                         }
        sample_ini_file = join(sample_texts_dir, 'en.ini')
        cfg = ConfigParser()
        cfg.read(sample_ini_file)
        ret = config_parser_to_dict(cfg)
        self.assertEqual(expected_dict, ret)

    def test_load_texts_for_generator(self):
        expected_dict = {'en': {'Section1': {'first': 'first', 'second': 'second'},
                                'Section2': {'third': 'third'},
                                'Section3': {'fourth': 'fourth', 'fifth': 'fifth', 'key': 'key', 'value': 'value'}
                                },
                         'sk': {'Section1': {'first': 'Prvý', 'second': 'Druhý'},
                                'Section2': {'third': 'Tretí'},
                                'Section3': {'fourth': 'Štvrtý', 'fifth': 'Piaty', 'key': 'Kľúč', 'value': 'Hodnota'}
                                }
                         }
        ret = load_texts_into_dict(sample_texts_dir)
        self.assertEqual(expected_dict, ret)

    def test_load_texts_into_config_parsers(self):
        ini_file = join(sample_texts_dir, 'en.ini')
        cfg_1 = ConfigParser()
        cfg_1.read(ini_file)

        ini_file = join(sample_texts_dir, 'sk.ini')
        cfg_2 = ConfigParser()
        cfg_2.read(ini_file)

        expected = {'en': cfg_1, 'sk': cfg_2}
        ret = load_texts_into_config_parsers(sample_texts_dir)
        self.assertEqual(expected, ret)

    def test_escape_underscore(self):
        chars_to_escape = ['&', '%', '$', '#', '_', '{', '}']
        for char in chars_to_escape:
            text = 'something' + char + 'something'
            expected = 'something\\' + char + 'something'
            ret = escape_latex_special_chars(text)
            self.assertEqual(expected, ret)

        text = 'something~something'
        expected = 'something\\textasciitilde{}something'
        ret = escape_latex_special_chars(text)
        self.assertEqual(expected, ret)

        text = 'something^something'
        expected = 'something\\^{}something'
        ret = escape_latex_special_chars(text)
        self.assertEqual(expected, ret)

        text = 'something\\something'
        expected = 'something\\textbackslash{}something'
        ret = escape_latex_special_chars(text)
        self.assertEqual(expected, ret)

        text = 'something<something'
        expected = 'something\\textless something'
        ret = escape_latex_special_chars(text)
        self.assertEqual(expected, ret)

        text = 'something>something'
        expected = 'something\\textgreater something'
        ret = escape_latex_special_chars(text)
        self.assertEqual(expected, ret)

    def test_convert_specs_to_seq_acc_no_specs(self):
        test_spec_list = []
        seq_acc_ret = convert_specs_to_seq_acc(test_spec_list)
        ret_sequences = seq_acc_ret.get_all_sequences()
        self.assertEqual(0, len(ret_sequences))

    def test_convert_specs_to_seq_acc_one_spec(self):
        test_spec_list = [TestFileSpecification(TestsIdData.test1_id, FileSpecification.RESULTS_FILE)]
        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)

        seq_acc_ret = convert_specs_to_seq_acc(test_spec_list)
        ret_sequences = seq_acc_ret.get_all_sequences()
        self.assertEqual(1, len(ret_sequences))

        ret = list(filter(lambda x: x.test_id == TestsIdData.test1_id, ret_sequences))[0]
        self.assertEqual(seq1, ret)

    def test_convert_specs_to_seq_acc_more_specs(self):
        test_spec_list = [TestFileSpecification(TestsIdData.test1_id, FileSpecification.RESULTS_FILE),
                          TestFileSpecification(TestsIdData.test2_id, FileSpecification.DATA_FILE, 1),
                          TestFileSpecification(TestsIdData.test3_id, FileSpecification.DATA_FILE, 2),
                          TestFileSpecification(TestsIdData.test4_id, FileSpecification.RESULTS_FILE),
                          TestFileSpecification(TestsIdData.test5_id, FileSpecification.RESULTS_FILE)]

        seq1 = PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS)
        seq2 = PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 1)
        seq3 = PValueSequence(TestsIdData.test3_id, PValuesFileType.DATA, 2)
        seq4 = PValueSequence(TestsIdData.test4_id, PValuesFileType.RESULTS)
        seq5 = PValueSequence(TestsIdData.test5_id, PValuesFileType.RESULTS)

        seq_acc_ret = convert_specs_to_seq_acc(test_spec_list)
        ret_sequences = seq_acc_ret.get_all_sequences()

        self.assertEqual(5, len(ret_sequences))

        ret = list(filter(lambda x: x.test_id == TestsIdData.test1_id, ret_sequences))[0]
        self.assertEqual(seq1, ret)

        ret = list(filter(lambda x: x.test_id == TestsIdData.test2_id, ret_sequences))[0]
        self.assertEqual(seq2, ret)

        ret = list(filter(lambda x: x.test_id == TestsIdData.test3_id, ret_sequences))[0]
        self.assertEqual(seq3, ret)

        ret = list(filter(lambda x: x.test_id == TestsIdData.test4_id, ret_sequences))[0]
        self.assertEqual(seq4, ret)

        ret = list(filter(lambda x: x.test_id == TestsIdData.test5_id, ret_sequences))[0]
        self.assertEqual(seq5, ret)

    def test_convert_specs_to_p_value_seq(self):
        specs = [TestFileSpecification(TestsIdData.test3_id, FileSpecification.RESULTS_FILE),
                 TestFileSpecification(TestsIdData.test4_id, FileSpecification.DATA_FILE, 5)]
        expected = [PValueSequence(TestsIdData.test3_id, PValuesFileType.RESULTS),
                    PValueSequence(TestsIdData.test4_id, PValuesFileType.DATA, 5)]
        ret = convert_specs_to_p_value_seq(specs)
        self.assertEqual(expected, ret)

    def test_list_difference_simple(self):
        a = [1, 2, 3, 4]
        b = [2, 3, 5]
        expected = [1, 4]
        ret = list_difference(a, b)
        self.assertEqual(expected, ret)

    def test_list_difference_more_complex(self):
        a = [1, 1, 1, 1, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6]
        b = [2, 3, 3, 5, 5]
        expected = [1, 1, 1, 1, 4, 4, 4, 6]
        ret = list_difference(a, b)
        self.assertEqual(expected, ret)

    def test_specs_list_to_p_value_seq_list_basic(self):
        specs = [[TestFileSpecification(TestsIdData.test3_id, FileSpecification.RESULTS_FILE),
                  TestFileSpecification(TestsIdData.test4_id, FileSpecification.DATA_FILE, 5)]]
        expected = [[PValueSequence(TestsIdData.test3_id, PValuesFileType.RESULTS),
                     PValueSequence(TestsIdData.test4_id, PValuesFileType.DATA, 5)]]
        ret = specs_list_to_p_value_seq_list(specs)
        self.assertEqual(expected, ret)

    def test_specs_list_to_p_value_seq_list_advanced(self):
        specs = [[TestFileSpecification(TestsIdData.test3_id, FileSpecification.RESULTS_FILE),
                  TestFileSpecification(TestsIdData.test4_id, FileSpecification.DATA_FILE, 5)],
                 [TestFileSpecification(TestsIdData.test1_id, FileSpecification.RESULTS_FILE),
                  TestFileSpecification(TestsIdData.test2_id, FileSpecification.DATA_FILE, 5),
                  TestFileSpecification(TestsIdData.test5_id, FileSpecification.DATA_FILE, 123)]]
        expected = [[PValueSequence(TestsIdData.test3_id, PValuesFileType.RESULTS),
                     PValueSequence(TestsIdData.test4_id, PValuesFileType.DATA, 5)],
                    [PValueSequence(TestsIdData.test1_id, PValuesFileType.RESULTS),
                     PValueSequence(TestsIdData.test2_id, PValuesFileType.DATA, 5),
                     PValueSequence(TestsIdData.test5_id, PValuesFileType.DATA, 123)]]
        ret = specs_list_to_p_value_seq_list(specs)
        self.assertEqual(expected, ret)

    def test_filter_arr_for_chart_x_axis_small_arr(self):
        arr = list(range(5))
        ret = filter_arr_for_chart_x_axis(arr)
        self.assertEqual(arr, ret)

        arr = list(range(20))
        ret = filter_arr_for_chart_x_axis(arr)
        self.assertEqual(arr, ret)

    def test_filter_arr_for_chart_x_axis_medium_arr(self):
        arr = list(range(21))
        expected = list(range(0, 21, 2))
        ret = filter_arr_for_chart_x_axis(arr)
        self.assertEqual(expected, ret)

        arr = list(range(39))
        expected = list(range(0, 39, 2))
        ret = filter_arr_for_chart_x_axis(arr)
        self.assertEqual(expected, ret)

        arr = list(range(100))
        expected = list(range(0, 100, 6))
        ret = filter_arr_for_chart_x_axis(arr)
        self.assertEqual(expected, ret)

    def test_filter_arr_for_chart_x_axis_large_arr(self):
        arr = list(range(999))
        expected = list(range(0, 999, 50))
        ret = filter_arr_for_chart_x_axis(arr)
        self.assertEqual(expected, ret)

        arr = list(range(1000))
        expected = list(range(0, 1000, 51))
        ret = filter_arr_for_chart_x_axis(arr)
        self.assertEqual(expected, ret)

        arr = list(range(10000))
        expected = list(range(0, 10000, 501))
        ret = filter_arr_for_chart_x_axis(arr)
        self.assertEqual(expected, ret)

    def test_filter_chart_x_ticks_raises(self):
        arr1 = [1]
        arr2 = [1, 2]
        with self.assertRaises(RuntimeError) as ex:
            filter_chart_x_ticks(arr1, arr2)
        self.assertEqual('Lists do not have the same length: (1, 2)', str(ex.exception))

    @patch('common.helper_functions.filter_arr_for_chart_x_axis', side_effect=['first', 'second'])
    def test_filter_chart_x_ticks(self, f_filter):
        arr1 = [1, 2, 3]
        arr2 = [3, 4, 5]
        ret1, ret2 = filter_chart_x_ticks(arr1, arr2)
        self.assertEqual('first', ret1)
        self.assertEqual('second', ret2)
        calls = [call(arr1), call(arr2)]
        f_filter.assert_has_calls(calls)
