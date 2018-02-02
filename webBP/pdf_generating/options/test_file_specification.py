from pdf_generating.options.file_specification import FileSpecification


class TestFileSpecification:
    def __init__(self, test_id: int, file_spec: FileSpecification, file_num: int=None):
        self.test_id = test_id
        self.file_spec = file_spec
        self.file_num = file_num
