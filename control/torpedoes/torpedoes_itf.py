"""
Module includes ITorpedoes
"""
import abc
from control.base_controller import BaseController


class ITorpedoes(BaseController, metaclass=abc.ABCMeta):
    """
    Interfce for control ROV's torpedo launcher
    """
    @abc.abstractmethod
    def is_torpedo_ready(self):
        """
        Check if torpedo is ready to lunch
        :return: True when torpedo is ready to lunch
        """
        pass

    @abc.abstractmethod
    def fire(self):
        """
        Lunch single torpedo
        """
        pass

    @abc.abstractmethod
    def power_laser(self, power_supplied):
        """
        Turn laser on or off
        :param power_supplied: True - laser is turned on
        """
        pass
