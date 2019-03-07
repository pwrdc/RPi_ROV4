"""
Module includes interface for depth sensor
"""
import abc
from sensors.base_sensor import BaseSensor


class IDepthSensor(BaseSensor):
    """
    Class for getting data from depth sensor by use of virtual file
    """
    @abc.abstractmethod
    def get_depth(self):
        """
        Get current distance behind ROV and water surface
        
        :return: single integer which represent depth of ROV in cm
        """
        pass
