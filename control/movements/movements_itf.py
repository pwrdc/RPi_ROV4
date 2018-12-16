"""
Module includes Interface for Movement Class
"""
import  abc

class IMovements(metaclass=abc.ABCMeta):
    """
    Interfce for algorithm for tasks
    """
    @abc.abstractmethod
    def set_lin_velocity(self, front, right, up):
        """ Set linear velocity
            in algorithm class do nothing
        """
        pass

    @abc.abstractmethod
    def set_ang_velocity(self, roll, pitch, yaw):
        """ Set angular velocity
        """
        pass

    @abc.abstractmethod
    def move_distance(self, front, right, up):
        """ Make precise linear movement
        For go back, left or down enter negative values
        """
        pass

    @abc.abstractmethod
    def rotate_angle(self, roll, pitch, yaw):
        """ Make precise angular movement
        """
        pass
