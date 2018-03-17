from abc import ABC, abstractmethod
from configparser import ConfigParser


class Err(ABC):
    @abstractmethod
    def get_message(self, texts: ConfigParser):
        pass
