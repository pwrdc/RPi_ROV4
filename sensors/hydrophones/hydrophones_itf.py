"""
Module includes interface for hydrophones class
"""
import abc
from sensors.base_sensor import BaseSensor


class IHydrophonesPair(BaseSensor, metaclass=abc.ABCMeta):
    """
    Interface for pair of hydrophones class
    """
    @abc.abstractmethod
    def get_angle(self):
        """
        Get angle behid main axisi of ROV and straight connecting poinger and ROV

        :return: single integer which represent angle behind x axis of ROV
        and straight connecting poinger and ROV
        """
        pass
