from configparser import ConfigParser
from os.path import dirname, abspath, join
from unittest import TestCase

from common.helper_functions import config_parser_to_dict, load_texts_into_dict, load_texts_into_config_parsers, \
    escape_latex_special_chars

this_dir = dirname(abspath(__file__))
sample_texts_dir = join(this_dir, '..', 'sample_files_for_tests', 'sample_texts')


class TestHelperFunctions(TestCase):
    def test_config_parser_to_dict(self):
        expected_dict = {'Section1': {'first': 'first', 'second': 'second'},
                         'Section2': {'third': 'third'},
                         'Section3': {'fourth': 'fourth', 'fifth': 'fifth', 'key': 'key', 'value': 'value'}
                         }
        sample_ini_file = join(sample_texts_dir, 'en.ini')
        cfg = ConfigParser()
        cfg.read(sample_ini_file)
        ret = config_parser_to_dict(cfg)
        self.assertEqual(expected_dict, ret)

    def test_load_texts_for_generator(self):
        expected_dict = {'en': {'Section1': {'first': 'first', 'second': 'second'},
                                'Section2': {'third': 'third'},
                                'Section3': {'fourth': 'fourth', 'fifth': 'fifth', 'key': 'key', 'value': 'value'}
                                },
                         'sk': {'Section1': {'first': 'Prvý', 'second': 'Druhý'},
                                'Section2': {'third': 'Tretí'},
                                'Section3': {'fourth': 'Štvrtý', 'fifth': 'Piaty', 'key': 'Kľúč', 'value': 'Hodnota'}
                                }
                         }
        ret = load_texts_into_dict(sample_texts_dir)
        self.assertEqual(expected_dict, ret)

    def test_load_texts_into_config_parsers(self):
        ini_file = join(sample_texts_dir, 'en.ini')
        cfg_1 = ConfigParser()
        cfg_1.read(ini_file)

        ini_file = join(sample_texts_dir, 'sk.ini')
        cfg_2 = ConfigParser()
        cfg_2.read(ini_file)

        expected = {'en': cfg_1, 'sk': cfg_2}
        ret = load_texts_into_config_parsers(sample_texts_dir)
        self.assertEqual(expected, ret)

    def test_escape_underscore(self):
        chars_to_escape = ['&', '%', '$', '#', '_', '{', '}']
        for char in chars_to_escape:
            text = 'something' + char + 'something'
            expected = 'something\\' + char + 'something'
            ret = escape_latex_special_chars(text)
            self.assertEqual(expected, ret)

        text = 'something~something'
        expected = 'something\\textasciitilde{}something'
        ret = escape_latex_special_chars(text)
        self.assertEqual(expected, ret)

        text = 'something^something'
        expected = 'something\\^{}something'
        ret = escape_latex_special_chars(text)
        self.assertEqual(expected, ret)

        text = 'something\\something'
        expected = 'something\\textbackslash{}something'
        ret = escape_latex_special_chars(text)
        self.assertEqual(expected, ret)

        text = 'something<something'
        expected = 'something\\textless something'
        ret = escape_latex_special_chars(text)
        self.assertEqual(expected, ret)

        text = 'something>something'
        expected = 'something\\textgreater something'
        ret = escape_latex_special_chars(text)
        self.assertEqual(expected, ret)
