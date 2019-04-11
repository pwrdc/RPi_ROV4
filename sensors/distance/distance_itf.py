"""
Module includes interface for distance sensor
"""
import abc
from sensors.base_sensor import BaseSensor


class IDistanceSensor(BaseSensor, metaclass=abc.ABCMeta):
    """
    Class for getting data from distance sensor by use of virtual file
    """
    @abc.abstractmethod
    def get_front_distance(self):
        '''
        Get distance from obsicle in front of ROV

        :return: single integer which represent distnace of obstacle in cm
        '''
        pass

