class PValuesChartDto:
    def __init__(self, alpha: float=0.01, x_label: str=None, y_label: str=None, title: str=None, zoomed: bool=False,
                 test_names: dict=None):
        self.alpha = alpha
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.zoomed = zoomed
        self.test_names = test_names
