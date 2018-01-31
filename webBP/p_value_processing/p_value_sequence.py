from p_value_processing.p_values_file_type import PValuesFileType


class PValueSequence:
    def __init__(self, test_id: int, p_values_file: PValuesFileType, data_num: int=None):
        self.test_id = test_id
        if p_values_file == PValuesFileType.RESULTS and data_num is not None:
            raise ValueError('data_num is not None, when using RESULTS file type')
        if p_values_file == PValuesFileType.DATA and data_num is None:
            raise ValueError('unspecified number of data file')
        if p_values_file == PValuesFileType.DATA and type(data_num) != int:
            raise TypeError('data_num has a wrong type ' + str(type(data_num)))
        self.p_values_file = p_values_file
        self.data_num = data_num

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(self, other.__class__):
            return self.test_id == other.test_id and self.p_values_file == other.p_values_file and \
                   self.data_num == other.data_num
        return False
