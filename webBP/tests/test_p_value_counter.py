import unittest
from os.path import abspath, dirname, join

from nist_statistics.p_value_counter import PValueCounter

this_dir = dirname(abspath(__file__))
file1 = join(this_dir, 'test_files', 'pvalues1.txt')
file2 = join(this_dir, 'test_files', 'pvalues2.txt')
file3 = join(this_dir, 'test_files', 'pvalues3.txt')


class PValueCounterTest(unittest.TestCase):
    def setUp(self):
        self.counter = PValueCounter()

    def test_reset(self):
        x = 0.01
        for i in range(0, 10):
            self.counter.get_num_into_array(x)
            x += 0.1
        for i in range(0, 10):
            self.assertTrue(self.counter.arr[i] > 0.0, 'Counter.arr[' + str(i) + '] is 0.0')
        self.counter.reset()
        for i in range(0, 10):
            self.assertTrue(self.counter.arr[i] < 0.000000001, 'Counter.arr[' + str(i) + '] is not 0.0')
        self.assertEqual(len(self.counter.get_p_values()), 0, 'raw p values are not reset')

    def test_file_load(self):
        self.counter.count_p_values_in_file(file1)
        my_arr = [0, 1, 0, 1, 3, 2, 1, 2, 0, 0]
        for i in range(0, 10):
            self.assertTrue(self.counter.arr[i] == my_arr[i], 'Counter.arr[' + str(i) + '] and my_array[' + str(i) +
                            '] are not the same')

    def test_alpha(self):
        self.counter.count_p_values_in_file(file2)
        self.assertEqual(self.counter.get_proportions(), 3 / 5, 'Proportions are not the same for the file ' + file2 +
                         ' with alpha ' + '0.05')

        another_counter = PValueCounter(0.05)
        another_counter.count_p_values_in_file(file2)
        self.assertEqual(another_counter.get_proportions(), 2 / 5,
                         'Proportions are not the same for the file ' + file2 +
                         ' with alpha ' + '0.05')

    def test_two_files_load(self):
        file1_arr = [0, 1, 0, 1, 3, 2, 1, 2, 0, 0]
        file3_arr = [0, 1, 1, 1, 0, 1, 0, 2, 2, 2]
        res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 10):
            res[i] = file1_arr[i] + file3_arr[i]
        self.counter.count_p_values_in_file(file1)
        self.counter.count_p_values_in_file(file3)
        for i in range(0, 10):
            self.assertTrue(self.counter.arr[i] == res[i], 'Counter.arr[' + str(i) + '] and res[' + str(i) +
                            '] are not the same')

    def test_loaded_pvalues(self):
        file1_p_values = [0.779952, 0.468925, 0.468925, 0.511232, 0.462545, 0.666913, 0.171598, 0.375557, 0.746548,
                        0.558648]
        self.counter.count_p_values_in_file(file1)
        self.assertEqual(file1_p_values, self.counter.get_p_values(), 'Loaded p_values from file are different than '
                                                                      'the expected ones')

        file2_p_values = [0.01, 0.02, 0.009, 0.11, 0.06]
        self.counter.count_p_values_in_file(file2)
        expected_p_values = file1_p_values + file2_p_values
        self.assertEqual(expected_p_values, self.counter.get_p_values(), 'Loaded p_values from file are different than '
                                                                         'the expected ones')