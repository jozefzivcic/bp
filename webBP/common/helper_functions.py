import math
import re
from configparser import ConfigParser

from os import listdir
from os.path import splitext, join

import numpy as np

from p_value_processing.p_value_sequence import PValueSequence
from p_value_processing.p_values_file_type import PValuesFileType
from p_value_processing.sequence_accumulator import SequenceAccumulator
from pdf_generating.options.file_specification import FileSpecification


def config_parser_to_dict(config_parser: ConfigParser):
    """
    Converts a ConfigParser object into a dictionary.

    The resulting dictionary contains sections as keys. For each key, there is another dictionary as a value, which
    contains keys and corresponding values from .ini file.
    :param config_parser: ConfigParser object
    """
    resulting_dict = {}
    for section in config_parser.sections():
        resulting_dict[section] = {}
        for key, val in config_parser.items(section):
            resulting_dict[section][key] = val
    return resulting_dict


def load_texts_into_dict(path_to_dir_with_texts: str) -> dict:
    ret = {}
    cfg = ConfigParser()
    for file in listdir(path_to_dir_with_texts):
        file_name, ext = splitext(file)
        if ext == '.ini':
            full_path = join(path_to_dir_with_texts, file)
            cfg.read(full_path)
            ret[file_name] = config_parser_to_dict(cfg)
    return ret


def load_texts_into_config_parsers(path_to_dir_with_texts: str) -> dict:
    ret = {}
    for file in listdir(path_to_dir_with_texts):
        file_name, ext = splitext(file)
        if ext == '.ini':
            full_path = join(path_to_dir_with_texts, file)
            cfg = ConfigParser()
            cfg.read(full_path)
            ret[file_name] = cfg
    return ret


def escape_latex_special_chars(text: str) -> str:
    """
    :param text: A plain text message.
    :return: The message escaped to appear correctly in LaTeX.
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless ',
        '>': r'\textgreater ',
    }
    regex = re.compile('|'.join(re.escape(key) for key in sorted(conv.keys(), key=lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)


def convert_specs_to_seq_acc(specs: list) -> SequenceAccumulator:
    seq_acc = SequenceAccumulator()
    for spec in specs:
        if spec.file_spec == FileSpecification.RESULTS_FILE:
            s = PValueSequence(spec.test_id, PValuesFileType.RESULTS)
        elif spec.file_spec == FileSpecification.DATA_FILE:
            s = PValueSequence(spec.test_id, PValuesFileType.DATA, spec.file_num)
        else:
            raise ValueError('Unsupported FileSpecification ' + str(spec.file_spec))
        seq_acc.add_sequence(s)
    return seq_acc


def convert_specs_to_p_value_seq(specs: list) -> list:
    ret = []
    for spec in specs:
        if spec.file_spec == FileSpecification.RESULTS_FILE:
            seq = PValueSequence(spec.test_id, PValuesFileType.RESULTS)
            ret.append(seq)
        elif spec.file_spec == FileSpecification.DATA_FILE:
            seq = PValueSequence(spec.test_id, PValuesFileType.DATA, spec.file_num)
            ret.append(seq)
        else:
            raise RuntimeError('Unknown file specification type: {}'.format(spec.file_spec))
    return ret


def specs_list_to_p_value_seq_list(specs_list: list) -> list:
    ret = []
    for specs in specs_list:
        s = convert_specs_to_p_value_seq(specs)
        ret.append(s)
    return ret


def list_difference(a: list, b: list) -> list:
    s = set(b)
    ret = [x for x in a if x not in s]
    return ret


def get_index_from_p_value(p_value: float, interval_length: float) -> int:
    pos = int(math.floor(p_value * 10))
    if pos >= 10:
        pos -= 1
    delta = int(round(interval_length / 0.1))
    ret = int(pos / delta)
    return ret


def insert_into_2d_array(values1: list, values2: list, arr_dim: int) -> np.ndarray:
    if len(values1) != len(values2):
        raise RuntimeError('Lists do not have the same size: ({}, {})'.format(len(values1), len(values2)))
    arr = np.zeros((arr_dim, arr_dim), dtype=np.uint64)
    interval_length = 1.0 / float(arr_dim)
    for i in range(len(values1)):
        v1 = values1[i]
        v2 = values2[i]
        x = get_index_from_p_value(v1, interval_length)
        y = get_index_from_p_value(v2, interval_length)
        arr[y][x] += 1
    return arr
