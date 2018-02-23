from enum import Enum


class TestsInChart(Enum):
    """
    Defines number of tests, from which data were taken to produce one chart.
    """
    SINGLE_TEST = 1,
    PAIR_OF_TESTS = 2,
    MULTIPLE_TESTS = 3
