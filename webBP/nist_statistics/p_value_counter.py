import math

from scipy.special import gammaincc

from nist_statistics.helpers import K
from nist_statistics.test_statistics_dto import TestStatisticsDTO


class PValueCounter:
    def __init__(self, alpha=0.01):
        self.alpha = alpha
        self.total_passed = 0
        self.total_tested = 0
        self.arr = []
        self.raw_p_values = []
        for i in range(0, 10):
            self.arr.append(0)

    def get_proportions(self):
        return self.total_passed / self.total_tested

    def get_p_values(self):
        return list(self.raw_p_values)

    def reset(self):
        self.total_passed = 0
        self.total_tested = 0
        for i in range(0, 10):
            self.arr[i] = 0
        self.raw_p_values = []

    def count_p_values_in_file(self, file):
        with open(file, 'r') as f:
            for line in f:
                if not line.isspace():
                    self.get_num_into_array(float(line))

    def get_num_into_array(self, num):
        if (num >= 0.0) and (num < 0.1):
            self.arr[0] += 1
        elif (num >= 0.1) and (num < 0.2):
            self.arr[1] += 1
        elif (num >= 0.2) and (num < 0.3):
            self.arr[2] += 1
        elif (num >= 0.3) and (num < 0.4):
            self.arr[3] += 1
        elif (num >= 0.4) and (num < 0.5):
            self.arr[4] += 1
        elif (num >= 0.5) and (num < 0.6):
            self.arr[5] += 1
        elif (num >= 0.6) and (num < 0.7):
            self.arr[6] += 1
        elif (num >= 0.7) and (num < 0.8):
            self.arr[7] += 1
        elif (num >= 0.8) and (num < 0.9):
            self.arr[8] += 1
        else:
            self.arr[9] += 1  # TODO: [0.9, 1.0) interval ???
        if num > self.alpha:
            self.total_passed += 1
        self.total_tested += 1
        self.raw_p_values.append(num)

    def generate_test_statistics_obj(self, test_name):
        test_statistics = TestStatisticsDTO()
        test_statistics.p_value_array = list(self.arr)
        test_statistics.total_passed = self.total_passed
        test_statistics.total_tested = self.total_tested
        test_statistics.p_value = self.compute_uniformity_p_value()
        test_statistics.test_name = test_name
        return test_statistics

    def compute_uniformity_p_value(self):
        sampleSize = self.total_tested
        expCount = int(sampleSize / 10)
        if expCount == 0:
            return 0.0
        chi2 = 0.0
        for pvalue in self.arr:
            chi2 += math.pow(pvalue - expCount, 2) / expCount
        return gammaincc(9.0 / 2.0, chi2 / 2.0)

    def compute_KS_p_value(self):
        Dmax = -1.0
        sampleSize = self.total_tested
        sorted_arr = sorted(self.raw_p_values)
        for j in range(1, sampleSize + 1):
            Dplus = math.fabs(j / float(sampleSize) - sorted_arr[j - 1])
            Dminus = math.fabs(sorted_arr[j - 1] - (j - 1) / float(sampleSize))

            if Dplus > Dmax:
                Dmax = Dplus
            if Dminus > Dmax:
                Dmax = Dminus

        return 1 - K(sampleSize, Dmax)
