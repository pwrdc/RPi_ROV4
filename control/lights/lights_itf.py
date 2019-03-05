"""
Module includes interface for Lights class
"""
import abc
from control.base_controller import BaseController


class ILights(BaseController, metaclass=abc.ABCMeta):
    """
    Interfce for control ROV's lights
    """
    @abc.abstractmethod
    def power_lights(self, power_supplied):
        """
        Turn lights on or off
        :param power_supplied: True - lights are turned on
        """
        pass
