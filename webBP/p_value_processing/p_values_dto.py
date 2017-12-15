class PValuesDto:
    def __init__(self, p_values: dict):
        self._p_values_dict = p_values

    def get_results_p_values(self):
        return self._p_values_dict['results']

    def get_data_p_values(self, file_num: int):
        key = 'data' + str(file_num)
        if not key in self._p_values_dict:
            raise ValueError('No data file with key: ' + str(file_num) + ' does not exists')
        return self._p_values_dict[key]
