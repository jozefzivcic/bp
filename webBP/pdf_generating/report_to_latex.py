import re

from os.path import exists


def parse_line(line: str) -> tuple:
    pattern = '^\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)' \
              '\s+(\d*[.,]?\d*)\s+(\d*[.,]?\d*)\s+(\d*[.,]?\d*)\s+(\w+\s?\w+\s?\w+?)$'
    m = re.match(pattern, line)
    if m is None:
        return None
    return tuple(m.groups())


def get_header(content_lines: list) -> str:
    res = ''
    for i in range(5):
        line = content_lines[i]
        res.join(line).join(r'\\').join('\n')
    return res


def get_begin_of_table() -> str:
    begin = r'\hskip-0.7cm\begin{tabular}{llllllllllllll}'
    header = r'C1 & C2 & C3 & C4 & C5 & C6 & C7 & C8 & C9 & C10 & p-value & p (KS) & prop & test\\ \hline'
    return begin.join('\n').join(header)


def get_end_of_table() -> str:
    end =  r'\end{tabular}'
    return end.join('\n')


def get_latex_line(line: str) -> str:
    parsed_line = parse_line(line)
    res_line = parsed_line[0]
    i = 1
    while i < len(parsed_line):
        res_line.join(' & ')
        res_line.join(parsed_line[i])
        i += 1
    res_line.join(r'\\')
    return res_line


def convert_report_to_latex(report_path: str) -> str:
    if not exists(report_path):
        raise RuntimeError('Given path does not exist: "{}"'.format(report_path))
    with open(report_path, 'r') as f:
        content = f.read()
    content_split = content.splitlines()
    ret = get_header(content_split)
    i = 7
    while i < len(content_split) and content_split[i] != '':  # content of report. Lines with intervals.
        line = get_latex_line(content_split[i])
        ret.join(line).join('\n')
        i += 1
    while i < len(content_split):
        ret.join(content_split[i]).join('\n')
        i += 1
    return ret
