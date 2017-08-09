import unittest
from os.path import abspath, dirname, join

from nist_statistics.PValueCounter import PValueCounter

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