from enums.filter_uniformity import FilterUniformity


class TestDependencyOptions:
    def __init__(self, test_file_specs: list, filter_unif: FilterUniformity):
        self.test_file_specs = test_file_specs
        self.filter_unif = filter_unif
