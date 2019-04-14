import abc
from control.base_controller import BaseController


class IManipulator(BaseController, metaclass=abc.ABCMeta):
    """
    Interface for manipulator control
    """
    @abc.abstractmethod
    def set_movements(self, first_param, second_param):
        """
        Control ROV's robotic arm
        """
        pass
