from unittest import TestCase

import math

from nist_statistics.helpers import K

values_for_K = [(10, 0.157153, 0.934603), (11, 0.129880, 0.980675), (12, 0.157413, 0.883136), (1, 0.857153, 0.285695),
                (20, 0.124485, 0.878815), (30, 0.152180, 0.446799), (50, 0.075664, 0.916313), (100, 0.084104, 0.454450),
                (1000, 0.086843, 0.000001)]

threshold = 0.00001


class TestFunctions(TestCase):
    def test_K(self):
        for elem in values_for_K:
            result = 1 - K(elem[0], elem[1])
            difference = math.fabs(result - elem[2])
            self.assertTrue(difference < threshold,
                            'Expected result is %8.6f, but computed is: %8.6f, difference is %8.6f' % (result, elem[2],
                                                                                                       difference))
