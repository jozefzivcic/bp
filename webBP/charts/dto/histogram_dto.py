class HistogramDto:
    def __init__(self, x_label: str=None, y_label: str=None, title: str=None, hist_for_tests: list=None):
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.hist_for_tests = hist_for_tests
