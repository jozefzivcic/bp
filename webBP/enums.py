from enum import Enum


class CreateErrors(Enum):
    length_none = 1
    length_greater_than_size = 2
    length_files = 3
    length_params_array = 4
    streams_less_than_one = 5
    special_param_not_in_range = 6
    ok = 7
    param_wrong_format = 8
