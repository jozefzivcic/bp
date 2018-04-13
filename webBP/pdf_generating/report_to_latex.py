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
        raise RuntimeError('Undifined name of test: "{}"'.format(name))


def get_shorten_test_name(t_type: NistTestType, texts: ConfigParser) -> str:
    pass


def parse_line(line: str) -> tuple:
    pattern = '^\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)' \
              '\s+(\d*[.,]?\d*)\s+(\d*[.,]?\d*)\s+(\d*[.,]?\d*)\s+(\w+\s?\w+\s?\w+?)$'
    m = re.match(pattern, line)
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
    begin = r'\hskip-0.7cm\begin{tabular}{llllllllllllll}' + '\n' \
            + r'C1 & C2 & C3 & C4 & C5 & C6 & C7 & C8 & C9 & C10 & p-value & p (KS) & prop & test\\ \hline'
    return begin


def get_end_of_table() -> str:
    end = r'\end{tabular}' + '\n'
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
    res_line += r'& {}\\'.format(shorten_name)
    return res_line


def convert_report_to_latex(report_path: str, texts: ConfigParser) -> str:
    if not exists(report_path):
        raise RuntimeError('Given path does not exist: "{}"'.format(report_path))
    with open(report_path, 'r') as f:
        content = f.read()
    content_split = content.splitlines()
    ret = get_header(content_split)
    i = 7
    while i < len(content_split) and content_split[i] != '':  # content of report. Lines with intervals.
        line = get_latex_line(content_split[i], texts)
        ret.join(line).join('\n')
        i += 1
    while i < len(content_split):
        ret.join(content_split[i]).join('\n')
        i += 1
    return ret
