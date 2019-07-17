import abc


class IManipulator(metaclass=abc.ABCMeta):
    """
    Interface for manipulator control
    """
    @abc.abstractmethod
    def set_movements(self, first_param, second_param):
        """
        Control ROV's robotic arm
        """
        pass

    @abc.abstractmethod
    def close_gripper(self, first_param, second_param):
        """
        Open gripper of ROV's robotic arm
        """
        pass

    @abc.abstractmethod
    def open_gripper(self, first_param, second_param):
        """
        Open gripper of ROV's robotic arm
        """
        pass
