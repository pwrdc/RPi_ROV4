"""
Module includes interface for depth sensor
"""
import abc
from sensors.base_sensor_itf import IBaseSensor


class IDepthSensor(IBaseSensor):
    """
    Class for getting data from depth sensor by use of virtual file
    """
    @abc.abstractmethod
    def get_depth(self):
        """
        :return: single integer which represent depth of ROV in cm
        """
        pass
