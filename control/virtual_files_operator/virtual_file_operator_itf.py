"""
Module include IVirtualFileOperator
"""
import abc


class IVirtualFileOperator(metaclass=abc.ABCMeta):
    """
    Interfce for control ROV movements
    """
    @abc.abstractmethod
    def __init__(self, file_name, directory=""):
        """
        :param file_name: string reppresenting name of virtual file
        :param directory: directory to virtual file
        """
        pass

    @abc.abstractmethod
    def read_data(self):
        """
        Set linear velocity as 100% of engines power
        :return: string read from virtual file
        """
        pass

    @abc.abstractmethod
    def send_data(self):
        """
        Save string to virtual file
        """
        pass
