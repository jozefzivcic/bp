class EcdfOptions:
    def __init__(self, test_file_specs: list):
        self.test_file_specs = test_file_specs

    def __repr__(self) -> str:
        return '<specs: "{}">'.format(repr(self.test_file_specs))
