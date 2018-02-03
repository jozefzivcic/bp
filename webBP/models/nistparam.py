class NistParam:
    def __init__(self):
        """
        Initializes object NistParam().
        """
        self.test_id = 0
        self.length = 0
        self.test_number = 0
        self.streams = 0
        self.special_parameter = None

    def has_special_parameter(self):
        """
        Returns if test can have optional parameter.
        :return: True if test can have parameter Block length, False otherwise.
        """
        if self.test_number == 2 or self.test_number == 8 or self.test_number == 9 or self.test_number == 11 or self.test_number == 14 or self.test_number == 15:
            return True
        return False

    def get_test_name(self):
        """
        Returns name for test.
        :return: Name of test.
        """
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
        """
        Returns block length name.
        :return: Block length name.
        """
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

    @staticmethod
    def get_default_param_value(test_number):
        """
        Returns default value of block length for given test.
        :param test_number: Test which default value of block length is returned.
        :return: If test can have an optional block length parameter, then is's default value, if can't then 0.
        """
        if test_number == 2:
            return 128
        elif test_number == 8:
            return 9
        elif test_number == 9:
            return 9
        elif test_number == 11:
            return 10
        elif test_number == 14:
            return 16
        elif test_number == 15:
            return 500
        return 0

    def set_default_param_value_according_to_test(self):
        """
        Sets block length parameter to default value.
        """
        self.special_parameter = self.get_default_param_value(self.test_number)

    def get_output_file_name(self, tested_file):
        """
        Creates output file name, that can be placed in .zip file. This method should be implemented by all
        attributes, if the code would be extended for another tests.
        :param tested_file: Name of file, which was tested for randomness.
        :return: File name.
        """
        length = 'length-' + str(self.length)
        streams = 'streams-' + str(self.streams)
        special_param = None
        if self.special_parameter is not None:
            special_param = 'blockLength-' + str(self.special_parameter)
            return '_'.join([tested_file, self.get_test_name(), length, streams,special_param])
        return '_'.join([tested_file, self.get_test_name(), length, streams])

    def get_num_of_data_files(self):
        if self.test_number == 1:
            return 0
        elif self.test_number == 2:
            return 0
        elif self.test_number == 3:
            return 2
        elif self.test_number == 4:
            return 0
        elif self.test_number == 5:
            return 0
        elif self.test_number == 6:
            return 0
        elif self.test_number == 7:
            return 0
        elif self.test_number == 8:
            return 148
        elif self.test_number == 9:
            return 0
        elif self.test_number == 10:
            return 0
        elif self.test_number == 11:
            return 0
        elif self.test_number == 12:
            return 8
        elif self.test_number == 13:
            return 18
        elif self.test_number == 14:
            return 2
        elif self.test_number == 15:
            return 0
        else:
            raise ValueError('Wrong test number ' + str(self.test_number))
