from charts.chart_info import ChartInfo
from charts.chart_type import ChartType
from charts.charts_storage_item import ChartsStorageItem
from common.error.err import Err
from common.info.info import Info


class ChartsStorage:
    def __init__(self):
        self._ch_info_list = []
        self._infos = {}
        self._errs = {}

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

    def add_infos_from_chart(self, ch_type: ChartType, infos: list):
        if ch_type in self._infos:
            raise RuntimeError('Infos for chart type {} already contained'.format(ch_type))
        self._infos[ch_type] = infos

    def add_errors_from_chart(self, ch_type: ChartType, errors: list):
        if ch_type in self._errs:
            raise RuntimeError('Errors for chart type {} already contained'.format(ch_type))
        self._errs[ch_type] = errors

    def extend(self, storage: 'ChartsStorage'):
        self._ch_info_list.extend(storage._ch_info_list)
        self._infos.update(storage._infos)
        self._errs.update(storage._errs)
        storage._ch_info_list = []
        storage._infos = {}
        storage._errs = {}

    def get_all_items(self) -> list:
        return list(self._ch_info_list)

    def get_infos_for_chart_type(self, ch_type: ChartType) -> list:
        return self._infos[ch_type]

    def get_infos_for_chart_type_safe(self, ch_type: ChartType) -> list:
        return self._infos.get(ch_type)

    def get_errors_for_chart_type(self, ch_type: ChartType) -> list:
        return self._errs[ch_type]

    def get_errors_for_chart_type_safe(self, ch_type: ChartType) -> list:
        return self._errs.get(ch_type)
