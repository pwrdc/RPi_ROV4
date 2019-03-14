"""
Module includes BaseSensor class
"""
import abc
from threading import Lock
from logpy import Logger
from control.base_controller import BaseController


class BaseSensor(BaseController, metaclass=abc.ABCMeta):
    """
    All sensors in sensors directory shoud inherit after this class
    """
    def __init__(self, main_logger=None, local_log=False, log_directory="",
                 log_timing=0.5):
        """
        :param main_logger: reference to external logger
        :param local_log: create local file with logs
        :param log_directory: directory for file with local logs
        :patam
        """
        super().__init__(main_logger, False, log_directory)

        self.local_logger = Logger(filename=self.__class__.__name__.lower(),
                                   directory=log_directory,
                                   title=self.__class__.__name__,
                                   external_function=self.getter2msg,
                                   internal_logger_time=log_timing)
        self.local_logger_lock = Lock()

    @abc.abstractmethod
    def getter2msg(self):
        """
        Convert data from class's getter/geters to log message
        :return: string containing single log message
        """
        pass
