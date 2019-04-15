"""
Module includes interface for Lights class
"""
import abc



class ILights(metaclass=abc.ABCMeta):
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
