class DifferentNumOfPValsError(Exception):
    def __init__(self, message: str, expected_len: int, actual_len: int):
        super(DifferentNumOfPValsError, self).__init__(message)
        self.expected_len = expected_len
        self.actual_len = actual_len
