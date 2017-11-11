import math

from scipy.special import gammaincc

from nist_statistics.helpers import K
from nist_statistics.test_statistics_dto import TestStatisticsDTO


class PValsProcessor:
    zero_threshold = 0.000000

    def __init__(self, alpha=0.01):
        self.alpha = alpha
        self.sample_size = 0
        self.arr = []
        self.raw_p_values = []
        for i in range(0, 10):
            self.arr.append(0)
        self.count = 0
        self.proportion = 0.0

    def get_proportions(self):
        return self.proportion

    def get_p_values(self):
        return list(self.raw_p_values)

    def reset(self):
        self.sample_size = 0
        for i in range(0, 10):
            self.arr[i] = 0
        self.raw_p_values = []
        self.count = 0
        self.proportion = 0.0

    def process_p_vals_in_file(self, file):
        with open(file, 'r') as f:
            for line in f:
                if not line.isspace():
                    self.get_num_into_array(float(line))
        if self.sample_size == 0:
            self.proportion = 0.0
        else:
            self.proportion = 1.0 - float(self.count / self.sample_size)

    def get_num_into_array(self, num):
        if num > PValsProcessor.zero_threshold:
            self.raw_p_values.append(num)
            self.sample_size += 1
            if num < self.alpha:
                self.count += 1
            self.get_p_value_to_interval(num)

    def get_p_value_to_interval(self, p_value):
        pos = int(math.floor(p_value) * 10)
        if pos >= 10:
            pos -= 1
        self.arr[pos] += 1

    def generate_test_statistics_obj(self, test_name):
        test_statistics = TestStatisticsDTO()
        test_statistics.alpha = self.alpha
        test_statistics.p_value_array = list(self.arr)
        test_statistics.sample_size = self.sample_size
        test_statistics.exp_count = int(self.sample_size / 10)
        test_statistics.uniformity_p_value = self.compute_uniformity_p_value()
        test_statistics.KS_p_value = self.compute_KS_p_value()
        test_statistics.test_name = test_name
        test_statistics.proportion = self.proportion
        test_statistics.proportion_threshold_min = self.get_proportion_threshold_min()
        test_statistics.proportion_threshold_max = self.get_proportion_threshold_max()
        return test_statistics

    def compute_uniformity_p_value(self):
        sampleSize = self.sample_size
        expCount = int(sampleSize / 10)
        if expCount == 0:
            return 0.0
        chi2 = 0.0
        for num in self.arr:
            chi2 += math.pow(num - expCount, 2) / expCount
        return gammaincc(9.0 / 2.0, chi2 / 2.0)

    def compute_KS_p_value(self):
        Dmax = -1.0
        sampleSize = self.sample_size
        sorted_arr = sorted(self.raw_p_values)
        for j in range(1, sampleSize + 1):
            Dplus = math.fabs(j / float(sampleSize) - sorted_arr[j - 1])
            Dminus = math.fabs(sorted_arr[j - 1] - (j - 1) / float(sampleSize))

            if Dplus > Dmax:
                Dmax = Dplus
            if Dminus > Dmax:
                Dmax = Dminus

        return 1 - K(sampleSize, Dmax)

    def get_proportion_threshold_min(self):
        p_hat = 1.0 - self.alpha
        return p_hat - 3.0 * math.sqrt((p_hat * self.alpha) / self.sample_size)

    def get_proportion_threshold_max(self):
        p_hat = 1.0 - self.alpha
        return p_hat + 3.0 * math.sqrt((p_hat * self.alpha) / self.sample_size)
