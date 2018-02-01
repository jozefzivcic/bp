import re
from configparser import ConfigParser

from os import listdir
from os.path import splitext, join


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


def check_for_uniformity(p_values1: list, p_values2: list):
    return False
