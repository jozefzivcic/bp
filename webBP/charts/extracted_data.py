from charts.data_source_info import DataSourceInfo
from common.error.err import Err
from common.info.info import Info


class ExtractedData:
    def __init__(self):
        self._data = []
        self._infos = []
        self._errors = []

    def add_data(self, ds_info: DataSourceInfo, data_for_drawer, info: Info=None, err: Err=None):
        self._data.append((ds_info, data_for_drawer, info, err))

    def add_info(self, info: Info):
        self._infos.append(info)

    def add_err(self, err: Err):
        self._errors.append(err)

    def get_all_data(self) -> list:
        return list(self._data)

    def get_all_infos(self) -> list:
        return list(self._infos)

    def get_all_errs(self) -> list:
        return list(self._errors)
