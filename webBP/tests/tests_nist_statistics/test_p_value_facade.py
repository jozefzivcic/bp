import json
from os.path import dirname, abspath, join
from unittest import TestCase
from unittest.mock import MagicMock

from nist_statistics.facade.PValueFacade import PValueFacade
from models.test import Test

this_dir = dirname(abspath(__file__))


class PValueFacadeTest(TestCase):
    def setUp(self):
        self.facade = PValueFacade(None)

    def test_get_json_p_value_intervals(self):
        self.facade.results_dao.get_path_for_test = MagicMock(return_value=join(this_dir, 'users', '4', 'tests_results',
                                                                                '14'))
        ret = self.facade.get_json_p_value_intervals_for_test(Test())
        arr = [['[0.0, 0.1)', 0], ['[0.1, 0.2)', 3], ['[0.2, 0.3)', 2], ['[0.3, 0.4)', 0], ['[0.4, 0.5)', 4],
        ['[0.5, 0.6)', 3], ['[0.6, 0.7)', 1], ['[0.7, 0.8)', 2], ['[0.8, 0.9)', 4], ['[0.9, 1.0]', 1]]
        data = {'data': arr}
        expected_output = json.dumps(data)
        self.assertEqual(ret, expected_output)
