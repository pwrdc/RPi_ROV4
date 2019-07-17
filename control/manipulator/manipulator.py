from control.manipulator.manipulator_itf import IManipulator
from control.base_controller import BaseController

class Manipulator(BaseController, IManipulator):

    def set_movements(self, first_param, second_param):
        """
        Control ROV's robotic arm
        """
        param = str(first_param)+','+str(second_param)
        self._send_data(param)

    def getter2msg(self):
        return 0

    def close_gripper(self):
        pass

    def open_gripper(self):
        pass
