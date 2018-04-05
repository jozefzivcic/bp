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

    def __lt__(self, other):
        if not isinstance(self, other.__class__):
            return False
        if self.test_id < other.test_id:
            return True
        if self.test_id > other.test_id:
            return False
        if self.p_values_file == PValuesFileType.RESULTS:
            return other.p_values_file == PValuesFileType.DATA
        if self.p_values_file == PValuesFileType.DATA:
            return other.p_values_file == PValuesFileType.DATA and self.data_num < other.data_num
        raise RuntimeError('Cannot compare such objects: {} and {}', str(self), str(other))

    def __le__(self, other):
        if not isinstance(self, other.__class__):
            return False
        if self.test_id < other.test_id:
            return True
        if self.test_id > other.test_id:
            return False
        if self.p_values_file == PValuesFileType.RESULTS:
            return True
        if self.p_values_file == PValuesFileType.DATA:
            return other.p_values_file == PValuesFileType.DATA and self.data_num <= other.data_num
        raise RuntimeError('Cannot compare such objects: {} and {}', str(self), str(other))

    def __hash__(self):
        return hash((self.test_id, self.p_values_file, self.data_num))

    def __str__(self):
        return '(test_id, file_type, data_num): (' + str(self.test_id) + ', ' + str(self.p_values_file) + ', '\
               + str(self.data_num) + ')'
