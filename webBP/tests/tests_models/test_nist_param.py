from enums.nist_test_type import NistTestType
from models.nistparam import NistParam
from unittest import TestCase


def get_all_except(test_type: NistTestType):
    ret = []
    for t_type in NistTestType:
        if t_type != test_type:
           ret.append(t_type)
    return ret


class TestNistParam(TestCase):
    def test_is_test_type(self):
        for i, test_type in enumerate(NistTestType):
            param = NistParam()
            param.test_number = i + 1
            self.assertTrue(param.is_test_type(test_type), 'test_number: {}, expected test type: {}'
                            .format(i + 1, test_type))
            for t_type in get_all_except(test_type):
                self.assertFalse(param.is_test_type(t_type))
