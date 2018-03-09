import numpy as np
from configparser import ConfigParser
from os.path import dirname, abspath, join
from unittest import TestCase

from common.helper_functions import config_parser_to_dict, load_texts_into_dict, load_texts_into_config_parsers, \
    escape_latex_special_chars, convert_specs_to_seq_acc, convert_specs_to_p_value_seq, list_difference, \
    specs_list_to_p_value_seq_list, insert_into_2d_array, get_index_from_p_value
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

    def test_get_index_from_p_value_basic_interval_length(self):
        values = np.arange(0.0, 1.1, step=0.1).tolist()
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.1)
            self.assertEqual(i, ret)

        values = np.arange(0.01, 1.1, step=0.1).tolist()
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.1)
            self.assertEqual(i, ret)

        values = np.arange(0.09999999999, 1.1, step=0.1).tolist()
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.1)
            self.assertEqual(i, ret)

    def test_get_index_from_p_value_doubled_interval_length(self):
        values = np.arange(0.0, 1.1, step=0.1).tolist()
        expected = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.2)
            self.assertEqual(expected[i], ret)

        values = np.arange(0.01, 1.1, step=0.1).tolist()
        expected = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.2)
            self.assertEqual(expected[i], ret)

        values = np.arange(0.09999999999, 1.1, step=0.1).tolist()
        expected = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        for i in range(10):
            ret = get_index_from_p_value(values[i], 0.2)
            self.assertEqual(expected[i], ret)

    def test_insert_into_2d_array_exception(self):
        with self.assertRaises(RuntimeError) as ex:
            insert_into_2d_array([1, 2, 3], [1, 2, 3, 4], 5)
        self.assertEqual('Lists do not have the same size: (3, 4)', str(ex.exception))

    def test_insert_into_2d_array_simple(self):
        values1 = [0.1, 0.3, 0.5, 0.7, 0.9]
        values2 = [0.0, 0.0, 0.0, 0.0, 0.0]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[1, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0]])
        self.assertTrue(np.array_equal(expected, ret))

    def test_insert_into_2d_array_all(self):
        values1 = [0.1, 0.3, 0.5, 0.7, 0.9,
                   0.1, 0.3, 0.5, 0.7, 0.9,
                   0.1, 0.3, 0.5, 0.7, 0.9,
                   0.1, 0.3, 0.5, 0.7, 0.9,
                   0.1, 0.3, 0.5, 0.7, 0.9]
        values2 = [0.1, 0.1, 0.1, 0.1, 0.1,
                   0.3, 0.3, 0.3, 0.3, 0.3,
                   0.5, 0.5, 0.5, 0.5, 0.5,
                   0.7, 0.7, 0.7, 0.7, 0.7,
                   0.9, 0.9, 0.9, 0.9, 0.9]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1],
                             [1, 1, 1, 1, 1]])
        self.assertTrue(np.array_equal(expected, ret))

    def test_insert_into_2d_array_border_values(self):
        values1 = [0.199999, 0.399999, 0.599999, 0.799999, 0.999999]
        values2 = [0.199999, 0.199999, 0.199999, 0.199999, 0.199999]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[1, 1, 1, 1, 1],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0]])
        self.assertTrue(np.array_equal(expected, ret))

        values1 = [0.199999, 0.399999, 0.599999, 0.799999, 0.999999]
        values2 = [0.999999, 0.999999, 0.999999, 0.999999, 0.999999]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [1, 1, 1, 1, 1]])
        self.assertTrue(np.array_equal(expected, ret))

        values1 = [0.199999, 0.199999, 0.199999, 0.199999, 0.199999]
        values2 = [0.199999, 0.399999, 0.599999, 0.799999, 0.999999]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[1, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0],
                             [1, 0, 0, 0, 0]])
        self.assertTrue(np.array_equal(expected, ret))

        values1 = [0.999999, 0.999999, 0.999999, 0.999999, 0.999999]
        values2 = [0.199999, 0.399999, 0.599999, 0.799999, 0.999999]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 1],
                             [0, 0, 0, 0, 1]])
        self.assertTrue(np.array_equal(expected, ret))

    def test_insert_into_2d_array_more_values_in_one_cell(self):
        values1 = [0.199999, 0.199999, 0.399999, 0.399999, 0.399999, 0.599999, 0.599999]
        values2 = [0.199999, 0.199999, 0.199999, 0.199999, 0.199999, 0.599999, 0.599999]
        ret = insert_into_2d_array(values1, values2, 5)
        expected = np.array([[2, 3, 0, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 2, 0, 0],
                             [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0]])
        self.assertTrue(np.array_equal(expected, ret))
