"""
Module includes IBaseSensor
"""
import abc


class IBaseSensor(metaclass=abc.ABCMeta):
    """
    All sensors in sensors directory shoud inherit after this class
    """
    @abc.abstractmethod
    def run(self):
        """
        This method is called by main thread to start
        all additional threads for sensor's object
        If class does not need separate thread,
        implement this method with pass
        """
        pass

    def close(self):
        """
        This method is called by main thread to close
        all additional threads for sensor's object
        and related activities
        If class does not need to close separate thread,
        implement this method with pass
        """
        pass
