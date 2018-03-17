from configparser import ConfigParser

from common.info.info import Info
from enums.filter_uniformity import FilterUniformity


class TestDepFilteredInfo(Info):
    def __init__(self, filtered_out: int, all_items: int, filter_unif: FilterUniformity):
        if filtered_out > all_items:
            raise ValueError('{} is greater than {}'.format(filtered_out, all_items))
        self._filtered_out = filtered_out
        self._all_items = all_items
        if filter_unif == FilterUniformity.DO_NOT_FILTER:
            raise ValueError('{} not allowed'.format(filter_unif))
        self._filter_unif = filter_unif

    def get_message(self, texts: ConfigParser):
        if self._filter_unif == FilterUniformity.REMOVE_UNIFORM:
            return texts.get('InfoTemplates', 'TestDepUnifFiltered').format(self._filtered_out, self._all_items)
        elif self._filter_unif == FilterUniformity.REMOVE_NON_UNIFORM:
            return texts.get('InfoTemplates', 'TestDepNonUnifFiltered').format(self._filtered_out, self._all_items)
        else:
            raise RuntimeError('{} not allowed'.format(self._filter_unif))

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self._filtered_out == other._filtered_out and self._all_items == other._all_items \
               and self._filter_unif == other._filter_unif
