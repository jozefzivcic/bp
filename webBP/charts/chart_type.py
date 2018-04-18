from enum import Enum
from functools import total_ordering


@total_ordering
class ChartType(Enum):
    """
    This enum represents possible types of charts, which can be generated.
    """
    P_VALUES = 1
    P_VALUES_ZOOMED = 2
    HISTOGRAM = 3
    TESTS_DEPENDENCY = 4
    ECDF = 5
    BOXPLOT_PT = 6
    PROPORTIONS = 7

    def __lt__(self, other):
        return self.value < other.value
