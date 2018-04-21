class DataForHistogramDrawer:
    def __init__(self, json_data_string: str=None, x_label: str=None, y_label: str=None, title: str=None):
        self.json_data_string = json_data_string
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
