from enum import Enum


class ChartType(Enum):
    """
    This enum represents possible types of charts, which can be generated.
    """
    P_VALUES = 1
    P_VALUES_ZOOMED = 2
    HISTOGRAM = 3
    TESTS_DEPENDENCY = 4
    ECDF = 5
