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


def load_texts_for_generator(path_to_dir_with_texts: str) -> dict:
    ret = {}
    cfg = ConfigParser()
    for file in listdir(path_to_dir_with_texts):
        file_name, ext = splitext(file)
        if ext == '.ini':
            full_path = join(path_to_dir_with_texts, file)
            cfg.read(full_path)
            ret[file_name] = config_parser_to_dict(cfg)
    return ret
