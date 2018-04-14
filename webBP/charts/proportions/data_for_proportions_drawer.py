class DataForProportionsDrawer(object):
    def __init__(self, title: str, x_label: str, y_label: str, y_lim_low: float, y_lim_high: float, x_ticks_pos: list,
                 x_ticks_lab: list, x_values: list, y_values: list, y_interval_low: float, y_interval_high: float,
                 y_interval_mid: float):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.y_lim_low = y_lim_low
        self.y_lim_high = y_lim_high
        self.x_ticks_pos = x_ticks_pos
        self.x_ticks_lab = x_ticks_lab
        self.x_values = x_values
        self.y_values = y_values
        self.y_interval_low = y_interval_low
        self.y_interval_high = y_interval_high
        self.y_interval_mid = y_interval_mid
