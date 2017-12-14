import unittest
from os.path import abspath, dirname, join

import math

from nist_statistics.p_vals_processor import PValsProcessor

this_dir = dirname(abspath(__file__))
file1 = join(this_dir, 'test_files', 'pvalues1.txt')
file2 = join(this_dir, 'test_files', 'pvalues2.txt')
file3 = join(this_dir, 'test_files', 'pvalues3.txt')
freq_pvalues = join(this_dir, 'test_files', 'frequency_pvalues.txt')
nine_pvalues = join(this_dir, 'test_files', 'nine_pvalues.txt')
block_freq_pvalues = join(this_dir, 'test_files', 'block_freq_pvalues.txt')
runs_pvalues = join(this_dir, 'test_files', 'runs_pvalues.txt')
zero_pvalues = join(this_dir, 'test_files', 'zero_pvalues.txt')


class PValsProcessorTest(unittest.TestCase):
    def setUp(self):
        self.processor = PValsProcessor()

    def helper_uniformity_p_value(self, expected: float, file: str):
        threshold = 0.000001
        self.processor.process_p_vals_in_file(file)
        res = self.processor.compute_uniformity_p_value()
        diff = math.fabs(res - expected)
        self.assertTrue(diff < threshold, 'Expected: %f, but got: %f' % (expected, res))

    def helper_KS_p_value(self, expected: float, file: str):
        threshold = 0.000003
        self.processor.process_p_vals_in_file(file)
        res = self.processor.compute_KS_p_value()
        diff = math.fabs(res - expected)
        self.assertTrue(diff < threshold, 'Expected: %f, but got: %f' % (expected, res))

    def test_reset(self):
        x = 0.01
        for i in range(0, 10):
            self.processor.get_num_into_array(x)
            x += 0.1
        for i in range(0, 10):
            self.assertTrue(self.processor.arr[i] == 1, 'Counter.arr[' + str(i) + '] is 0')
        self.assertTrue(len(self.processor.raw_p_values) > 0)
        self.assertEqual(self.processor.sample_size,  10)
        self.processor.count = 5
        self.processor.reset()
        for i in range(0, 10):
            self.assertTrue(self.processor.arr[i] == 0, 'Counter.arr[' + str(i) + '] is not 0.0')
        self.assertTrue(len(self.processor.raw_p_values) == 0)
        self.assertEqual(len(self.processor.get_p_values()), 0, 'raw p values are not reset')
        self.assertEqual(self.processor.sample_size, 0)
        self.assertEqual(self.processor.count, 0)

    def test_file_load(self):
        self.processor.process_p_vals_in_file(file1)
        my_arr = [0, 1, 0, 1, 3, 2, 1, 2, 0, 0]
        for i in range(0, 10):
            self.assertTrue(self.processor.arr[i] == my_arr[i], 'Counter.arr[' + str(i) + '] and my_array[' + str(i) +
                            '] are not the same')

    def test_skip_zero_pvalues(self):
        self.processor.process_p_vals_in_file(zero_pvalues)
        self.assertEqual(len(self.processor.raw_p_values), 0)

    def test_proportions_zero_pvalues(self):
        self.processor.process_p_vals_in_file(zero_pvalues)
        self.assertEqual(self.processor.get_proportions(), 0.0, 'Proportions are not the same for the file ' + file2 +
                         ' with alpha ' + str(self.processor.alpha))

    def test_proportions_default_alpha(self):
        self.processor.process_p_vals_in_file(file2)
        self.assertEqual(self.processor.get_proportions(), 0.8, 'Proportions are not the same for the file ' + file2 +
                         ' with alpha ' + str(self.processor.alpha))

    def test_proportions_changed_alpha(self):
        pvals_processor = PValsProcessor(0.05)
        pvals_processor.process_p_vals_in_file(file2)
        self.assertEqual(pvals_processor.get_proportions(), 0.4, 'Proportions are not the same for the file ' + file2 +
                         ' with alpha ' + str(self.processor.alpha))

    def test_two_files_load(self):
        file1_arr = [0, 1, 0, 1, 3, 2, 1, 2, 0, 0]
        file3_arr = [0, 1, 1, 1, 0, 1, 0, 2, 2, 2]
        res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 10):
            res[i] = file1_arr[i] + file3_arr[i]
        self.processor.process_p_vals_in_file(file1)
        self.processor.process_p_vals_in_file(file3)
        for i in range(0, 10):
            self.assertTrue(self.processor.arr[i] == res[i], 'Counter.arr[' + str(i) + '] and res[' + str(i) +
                            '] are not the same')

    def test_loaded_pvalues(self):
        file1_p_values = [0.779952, 0.468925, 0.468925, 0.511232, 0.462545, 0.666913, 0.171598, 0.375557, 0.746548,
                          0.558648]
        self.processor.process_p_vals_in_file(file1)
        self.assertEqual(file1_p_values, self.processor.get_p_values(), 'Loaded p_values from file are different than '
                                                                      'the expected ones')

        file2_p_values = [0.01, 0.02, 0.009, 0.11, 0.06]
        self.processor.process_p_vals_in_file(file2)
        expected_p_values = file1_p_values + file2_p_values
        self.assertEqual(expected_p_values, self.processor.get_p_values(), 'Loaded p_values from file are different than '
                                                                         'the expected ones')

    def test_compute_uniformity_p_value_zero(self):
        self.helper_uniformity_p_value(0.0, file2)

    def test_compute_uniformity_p_value_zero_2(self):
        self.helper_uniformity_p_value(0.0, nine_pvalues)

    def test_compute_uniformity_p_value(self):
        self.helper_uniformity_p_value(0.090936, freq_pvalues)

    def test_compute_uniformity_p_value_2(self):
        self.helper_uniformity_p_value(0.350485, block_freq_pvalues)

    def test_compute_uniformity_p_value_runs(self):
        self.helper_uniformity_p_value(0.082177, runs_pvalues)

    def test_compute_KS_p_value(self):
        self.helper_KS_p_value(0.767161, freq_pvalues)

    def test_compute_KS_p_value_2(self):
        self.helper_KS_p_value(0.654596, block_freq_pvalues)

    def test_compute_KS_p_value_runs(self):
        self.helper_KS_p_value(0.265525, runs_pvalues)

    def test_proportions_threshold_min(self):
        self.processor.sample_size = 10
        result = self.processor.get_proportion_threshold_min()
        expected = 0.895607
        threshold = 0.0000003
        diff = math.fabs(result - expected)
        self.assertTrue(diff < threshold, 'Expected: ' + str(expected) + ', but got: ' + str(result))

    def test_proportions_threshold_max(self):
        self.processor.sample_size = 10
        result = self.processor.get_proportion_threshold_max()
        expected = 1.084393
        threshold = 0.0000003
        diff = math.fabs(result - expected)
        self.assertTrue(diff < threshold, 'Expected: ' + str(expected) + ', but got: ' + str(result))

    def test_generate_test_statistics_dto(self):
        threshold = 0.000003
        test_name = 'test_name'
        self.processor.process_p_vals_in_file(freq_pvalues)
        dto = self.processor.generate_test_statistics_obj(test_name)
        expected_p_value_arr = [0, 2, 3, 0, 3, 1, 2, 2, 0, 2]
        expected_unif_p_value = 0.090936
        expected_KS_pvalue = 0.767161
        expected_sample_size = 15

        self.assertEqual(expected_p_value_arr, dto.p_value_array)

        self.assertEqual(dto.sample_size, expected_sample_size)

        self.assertEqual(dto.test_name, test_name)

        self.assertEqual(dto.exp_count, 1)

        diff = math.fabs(dto.uniformity_p_value - expected_unif_p_value)
        self.assertTrue(diff < threshold, 'Expected: %f, but got: %f' % (expected_unif_p_value, dto.uniformity_p_value))

        diff = math.fabs(dto.KS_p_value - expected_KS_pvalue)
        self.assertTrue(diff < threshold, 'Expected: %f, but got: %f' % (expected_KS_pvalue, dto.KS_p_value))

        self.assertEqual(dto.proportion, 1.0)

        p_hat = 1.0 - self.processor.alpha

        thr_min = p_hat - 3.0 * math.sqrt((p_hat * self.processor.alpha) / expected_sample_size)
        self.assertEqual(dto.proportion_threshold_min, thr_min)

        thr_max = p_hat + 3.0 * math.sqrt((p_hat * self.processor.alpha) / expected_sample_size)
        self.assertEqual(dto.proportion_threshold_max, thr_max)
