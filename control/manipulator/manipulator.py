from control.manipulator.manipulator_itf import IManipulator

class Manipulator(IManipulator):

    def set_movements(self, first_param, second_param):
        """
        Control ROV's robotic arm
        """
        self._send_data([first_param,second_param])

    def getter2msg(self):
        return 0