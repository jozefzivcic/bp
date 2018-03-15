from enum import Enum


class FilterUniformity(Enum):
    DO_NOT_FILTER = 0,
    REMOVE_UNIFORM = 1,
    REMOVE_NON_UNIFORM = 2
