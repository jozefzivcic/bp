class ChartInfo:
    def __init__(self, path=None, chart_type=None, file_id=None):
        self.path_to_chart = path
        self.chart_type = chart_type
        self.file_id = file_id

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self.path_to_chart == other.path_to_chart and self.chart_type == other.chart_type and \
               self.file_id == other.file_id
