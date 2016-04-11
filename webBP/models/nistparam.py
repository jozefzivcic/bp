class NistParam:
    def __init__(self):
        self.test_id = 0
        self.length = 0
        self.test_number = 0
        self.streams = 0
        self.special_parameter = None

    def has_special_parameter(self):
        if self.test_number == 2 or self.test_number == 8 or self.test_number == 9 or self.test_number == 11 or self.test_number == 14 or self.test_number == 15:
            return True
        return False

    def get_test_name(self):
        if self.test_number == 1:
            return 'Frequency'
        elif self.test_number == 2:
            return 'Block Frequency'
        elif self.test_number == 3:
            return 'Cumulative Sums'
        elif self.test_number == 4:
            return 'Runs'
        elif self.test_number == 5:
            return 'Longest Run of Ones'
        elif self.test_number == 6:
            return 'Rank'
        elif self.test_number == 7:
            return 'Discrete Fourier Transform'
        elif self.test_number == 8:
            return 'Nonperiodic Template Matchings'
        elif self.test_number == 9:
            return 'Overlapping Template Matchings'
        elif self.test_number == 10:
            return 'Universal Statistical'
        elif self.test_number == 11:
            return 'Approximate Entropy'
        elif self.test_number == 12:
            return 'Random Excursions'
        elif self.test_number == 13:
            return 'Random Excursions Variant'
        elif self.test_number == 14:
            return 'Serial'
        elif self.test_number == 15:
            return 'Linear Complexity'
        return 'None'

    def get_special_parameter_name(self):
        if self.test_number == 2:
            return 'block length(M)'
        elif self.test_number == 8:
            return 'block length(m)'
        elif self.test_number == 9:
            return 'block length(m)'
        elif self.test_number == 11:
            return 'block length(m)'
        elif self.test_number == 14:
            return 'block length(m)'
        elif self.test_number == 15:
            return 'block length(M)'
        return 'None'

    def get_default_param_value(self):
        if self.test_number == 2:
            return 128
        elif self.test_number == 8:
            return 9
        elif self.test_number == 9:
            return 9
        elif self.test_number == 11:
            return 10
        elif self.test_number == 14:
            return 16
        elif self.test_number == 15:
            return 500
        return 0

    def set_default_param_value_according_to_test(self):
        self.special_parameter = self.get_default_param_value()
