class DataForEcdfDrawer:
    def __init__(self, alpha: float=0.01, title: str=None, x_label: str=None, y_label: str=None,
                 empirical_label: str=None, theoretical_label: str=None, p_values: list=None, ci_x_start: float=None,
                 ci_x_end: float=None, ci_y_start: float=None, ci_y_end: float=None):
        self.alpha = alpha
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.empirical_label = empirical_label
        self.theoretical_label = theoretical_label
        self.p_values = p_values
        self.ci_x_start = ci_x_start
        self.ci_x_end = ci_x_end
        self.ci_y_start = ci_y_start
        self.ci_y_end = ci_y_end
