class NistParam:
    def __init__(self):
        self.test_id = 0
        self.length = 0
        self.test_number = 0
        self.streams = 0
        self.special_parameter = 0

    def has_special_parameter(self):
        if self.test_number == 2 or self.test_number == 8 or self.test_number == 9 or self.test_number == 11 or self.test_number == 14 or self.test_number == 15:
            return True
        return False