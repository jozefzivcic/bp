from configparser import ConfigParser

from common.info.info import Info


class TestDepUnifInfo(Info):
    def __init__(self, p_value: float, condition_fulfillment: bool):
        self._p_value = p_value
        self._condition_fulfillment = condition_fulfillment

    def get_message(self, texts: ConfigParser):
        if self._condition_fulfillment:
            return texts.get('InfoTemplates', 'TestDepUnifInfoT').format(self._p_value)
        else:
            return texts.get('InfoTemplates', 'TestDepUnifInfoF').format(self._p_value)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self._p_value == other._p_value and self._condition_fulfillment == other._condition_fulfillment
