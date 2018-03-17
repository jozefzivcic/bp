from os.path import exists

from os import remove

from charts.chart_info import ChartInfo
from charts.charts_storage_item import ChartsStorageItem
from common.error.err import Err
from common.info.info import Info


class ChartsStorage:
    def __init__(self):
        self._ch_info_list = []

    def add_chart_info(self, chart_info: ChartInfo, info: Info=None, err: Err=None):
        if chart_info is None:
            raise TypeError('Chart info is None')
        if chart_info.path_to_chart is None:
            raise TypeError('Path to chart is None')
        if chart_info.chart_type is None:
            raise TypeError('Chart type is None')
        if chart_info.file_id is None:
            raise TypeError('file_id in chart_info is None')

        cs_item = ChartsStorageItem(chart_info, info, err)
        self._ch_info_list.append(cs_item)

    def extend(self, storage: 'ChartsStorage'):
        self._ch_info_list.extend(storage._ch_info_list)
        storage._ch_info_list = []

    def get_all_items(self) -> list:
        return list(self._ch_info_list)
