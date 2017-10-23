from unittest import TestCase

import math
from scipy.special import gammaincc

results = [(4.500000, 3.166667, 0.706149), (4.500000, 6.666667, 0.148094), (4.500000, 5.950000, 0.219006),
           (4.500000, 6.280000, 0.183547), (4.500000, 6.700000, 0.145326), (4.500000, 7.257143, 0.105171),
           (4.500000, 6.775000, 0.139257), (4.500000, 7.800000, 0.075719), (4.500000, 8.540000, 0.047478),
           (4.500000, 10.600000, 0.011791), (4.500000, 10.910714, 0.009462), (4.500000, 10.919643, 0.009403)]


class GammaincTest(TestCase):
    def test_gammainc(self):
        threshold = 0.000001
        for elem in results:
            res = gammaincc(elem[0], elem[1])
            difference = math.fabs(res - elem[2])
            self.assertTrue(difference < threshold, 'Expected %8.6f, computed %8.6f, difference %8.6f' % (elem[2], res,
                                                                                                          difference))
