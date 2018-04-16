from configparser import ConfigParser

from common.error.err import Err


class PropDiffLenErr(Err):
    def __init__(self, expected_len, actual_len):
        if expected_len == actual_len:
            raise ValueError('Expected and actual lengths are the same: {}'.format(expected_len))
        self.expected_len = expected_len
        self.actual_len = actual_len

    def get_message(self, texts: ConfigParser):
        template = texts.get('ErrTemplates', 'PropDiffLen')
        return template.format(self.expected_len, self.actual_len)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False
        return self.expected_len == other.expected_len and self.actual_len == other.actual_len
