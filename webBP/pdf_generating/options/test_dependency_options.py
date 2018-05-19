from enums.filter_uniformity import FilterUniformity
from enums.test_dep_pairs import TestDepPairs


class TestDependencyOptions:
    def __init__(self, test_file_specs: list, filter_unif: FilterUniformity, test_pairs: TestDepPairs):
        self.test_file_specs = test_file_specs
        self.filter_unif = filter_unif
        self.test_pairs = test_pairs

    def __repr__(self) -> str:
        return '<specs: "{}", filter unif: "{}", test pairs: "{}">'.format(self.test_file_specs, repr(self.filter_unif),
                                                                           repr(self.test_pairs))
