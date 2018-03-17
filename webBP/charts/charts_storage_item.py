from charts.chart_info import ChartInfo
from common.error.err import Err
from common.info.info import Info


class ChartsStorageItem:
    def __init__(self, ch_info: ChartInfo, info: Info=None, err: Err=None):
        self.ch_info = ch_info
        self.info = info
        self.err = err

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self.ch_info == other.ch_info and self.info == other.info and self.err == other.err
