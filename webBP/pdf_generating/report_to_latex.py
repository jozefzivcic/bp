import re
from configparser import ConfigParser

from os.path import exists

from common.helper_functions import escape_latex_special_chars
from enums.nist_test_type import NistTestType


def get_test_type_from_name(name: str) -> NistTestType:
    if name == 'Frequency':
        return NistTestType.TEST_FREQUENCY
    elif name == 'Block Frequency':
        return NistTestType.TEST_BLOCK_FREQUENCY
    elif name == 'Cumulative Sums':
        return NistTestType.TEST_CUSUM
    elif name == 'Runs':
        return NistTestType.TEST_RUNS
    elif name == 'Longest Run of Ones':
        return NistTestType.TEST_LONGEST_RUN
    elif name == 'Rank':
        return NistTestType.TEST_RANK
    elif name == 'Discrete Fourier Transform':
        return NistTestType.TEST_FFT
    elif name == 'Nonperiodic Template Matchings':
        return NistTestType.TEST_NONPERIODIC
    elif name == 'Overlapping Template Matchings':
        return NistTestType.TEST_OVERLAPPING
    elif name == 'Universal Statistical':
        return NistTestType.TEST_UNIVERSAL
    elif name == 'Approximate Entropy':
        return NistTestType.TEST_APEN
    elif name == 'Random Excursions':
        return NistTestType.TEST_RND_EXCURSION
    elif name == 'Random Excursions Variant':
        return NistTestType.TEST_RND_EXCURSION_VAR
    elif name == 'Serial':
        return NistTestType.TEST_SERIAL
    elif name == 'Linear Complexity':
        return NistTestType.TEST_LINEARCOMPLEXITY
    else:
        raise RuntimeError('Undefined name of test: "{}"'.format(name))


def get_shorten_test_name(t_type: NistTestType, texts: ConfigParser) -> str:
    if t_type == NistTestType.TEST_FREQUENCY:
        return texts.get('ShortNames', 'Freq')
    elif t_type == NistTestType.TEST_BLOCK_FREQUENCY:
        return texts.get('ShortNames', 'BFreq')
    elif t_type == NistTestType.TEST_CUSUM:
        return texts.get('ShortNames', 'CuSums')
    elif t_type == NistTestType.TEST_RUNS:
        return texts.get('ShortNames', 'Runs')
    elif t_type == NistTestType.TEST_LONGEST_RUN:
        return texts.get('ShortNames', 'LongRun')
    elif t_type == NistTestType.TEST_RANK:
        return texts.get('ShortNames', 'Rank')
    elif t_type == NistTestType.TEST_FFT:
        return texts.get('ShortNames', 'FFT')
    elif t_type == NistTestType.TEST_NONPERIODIC:
        return texts.get('ShortNames', 'Nonperiodic')
    elif t_type == NistTestType.TEST_OVERLAPPING:
        return texts.get('ShortNames', 'Overlapping')
    elif t_type == NistTestType.TEST_UNIVERSAL:
        return texts.get('ShortNames', 'Universal')
    elif t_type == NistTestType.TEST_APEN:
        return texts.get('ShortNames', 'Approx')
    elif t_type == NistTestType.TEST_RND_EXCURSION:
        return texts.get('ShortNames', 'RandExcs')
    elif t_type == NistTestType.TEST_RND_EXCURSION_VAR:
        return texts.get('ShortNames', 'RandExcsVar')
    elif t_type == NistTestType.TEST_SERIAL:
        return texts.get('ShortNames', 'Serial')
    elif t_type == NistTestType.TEST_LINEARCOMPLEXITY:
        return texts.get('ShortNames', 'Linear')
    else:
        raise RuntimeError('Undefined type of test: "{}"'.format(t_type))


def parse_line(line: str) -> tuple:
    m = re.match(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)'
                 r'\s+(\d*[.,]?\d*(?:\s+\*)?|----)'
                 r'\s+(\d*[.,]?\d*(?:\s+\*)?|----)'
                 r'\s+(\d*[.,]?\d*(?:\s+\*)?|----)'
                 r'\s+(\w+\s?\w+\s?\w+\s?\w+?)$', line)
    if m is None:
        return None
    return tuple(m.groups())


def get_header(content_lines: list) -> str:
    res = ''
    end_line = r'\\' + '\n'
    for i in range(5):
        line = content_lines[i]
        res += escape_latex_special_chars(line)
        res += end_line
    return res


def get_begin_of_table() -> str:
    begin = r'\hskip-0.7cm\begin{longtable}{llllllllllllll}' + '\n' \
            + r'C1 & C2 & C3 & C4 & C5 & C6 & C7 & C8 & C9 & C10 & p-value & p (KS) & prop & test\\ \hline' + '\n'
    return begin


def get_end_of_table() -> str:
    end = r'\end{longtable}' + '\n'
    return end


def get_latex_line(line: str, texts: ConfigParser) -> str:
    parsed_line = parse_line(line)
    if parsed_line is None:
        raise RuntimeError('Wrong format of line: "{}"'.format(line))
    res_line = parsed_line[0]
    i = 1
    while i < len(parsed_line) - 1:
        res_line += ' & '
        res_line += parsed_line[i]
        i += 1
    t_type = get_test_type_from_name(parsed_line[-1])
    shorten_name = get_shorten_test_name(t_type, texts)
    res_line += r' & {}\\'.format(shorten_name)
    return res_line


def convert_report_to_latex(report_path: str, texts: ConfigParser) -> str:
    if not exists(report_path):
        raise RuntimeError('Given path does not exist: "{}"'.format(report_path))
    if texts is None:
        raise RuntimeError('Texts cannot be None')
    with open(report_path, 'r') as f:
        content = f.read()
    content_split = content.splitlines()
    ret = get_header(content_split)
    ret += get_begin_of_table()
    i = 7
    while i < len(content_split) and content_split[i] != '':  # content of report. Lines with intervals.
        line = get_latex_line(content_split[i], texts)
        ret += line
        ret += '\n'
        i += 1
    ret += get_end_of_table()
    while i < len(content_split):
        ret += content_split[i]
        if content_split[i] != '':
            ret += r'\\'
        ret += '\n'
        i += 1
    return ret
