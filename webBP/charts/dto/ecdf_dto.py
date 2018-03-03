class EcdfDto:
    def __init__(self, alpha: float=0.01, title: str=None, x_label: str=None, y_label: str=None,
                 empirical_label: str=None, theoretical_label: str=None, sequences: list=None):
        self.alpha = alpha
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.empirical_label = empirical_label
        self.theoretical_label = theoretical_label
        self.sequences = sequences
