from p_value_processing.data_file_error import DataFileError


class PValuesDto:
    max_num_of_data_files = 256

    def __init__(self, p_values: dict):
        self.check_data_files(p_values)
        self._p_values_dict = p_values

    def get_results_p_values(self):
        return self._p_values_dict['results']

    def get_data_p_values(self, file_num: int):
        key = 'data' + str(file_num)
        if not key in self._p_values_dict:
            raise ValueError('No data file with key: ' + str(file_num) + ' does not exists')
        return self._p_values_dict[key]

    def get_data_files_indices(self) -> list:
        ret = []
        for i in range(1, PValuesDto.max_num_of_data_files + 1):
            if ('data' + str(i)) not in self._p_values_dict:
                break
            ret.append(i)
        if not ret:
            raise DataFileError('No data file')
        ret.sort()
        return ret

    def has_data_files(self) -> bool:
        try:
            self.get_data_files_indices()
        except DataFileError:
            return False
        return True

    def check_data_files(self, p_values):
        counter = 0
        for i in range(1, PValuesDto.max_num_of_data_files + 2):
            if ('data' + str(i)) not in p_values:
                break
            counter += 1
        if counter > PValuesDto.max_num_of_data_files:
            raise DataFileError('Too many data files. Allowed maximum is ' + str(PValuesDto.max_num_of_data_files))
