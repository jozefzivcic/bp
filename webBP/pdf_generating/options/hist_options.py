class HistOptions(object):
    def __init__(self, hist_for_tests: list):
        self.hist_for_tests = hist_for_tests

    def __repr__(self) -> str:
        return '<hist_for_tests: "{}">'.format(repr(self.hist_for_tests))
