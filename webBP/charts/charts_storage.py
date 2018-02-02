from os.path import exists

from os import remove

from charts.chart_info import ChartInfo


class ChartsStorage:
    def __init__(self):
        self._info_list = []

    def add_chart_info(self, chart_info: ChartInfo):
        if chart_info is None:
            raise TypeError('Chart info is None')
        if chart_info.path_to_chart is None:
            raise TypeError('Path to chart is None')
        if chart_info.chart_type is None:
            raise TypeError('Chart type is None')
        if chart_info.file_id is None:
            raise TypeError('file_id in chart_info is None')

        self._info_list.append(chart_info)

    def extend(self, storage: 'ChartsStorage'):
        self._info_list.extend(storage._info_list)
        storage._info_list = []

    def get_all_infos(self) -> list:
        return list(self._info_list)

    def delete_files_on_paths(self):
        for chart_info in self._info_list:
            if exists(chart_info.path_to_chart):
                remove(chart_info.path_to_chart)
