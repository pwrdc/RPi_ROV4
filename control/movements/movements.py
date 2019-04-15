"""

Module includes Movemnets clas
"""
from control.movements.movements_itf import IMovements
from control.pid.pid import PID
from control.base_controller import BaseController

LOOP_DELAY = 0.05

# TODO - delete or move pyro server to communication (replace or integrate with communication for xavier)

class Movements(BaseController,IMovements):
    """
    Interfce for algorithm for accesing rpi Movement Class
    """
    def __init__(self,port, depth_sensor_ref, ahrs_ref, main_logger=None,
    local_log=False):
        super().__init__(port = port, main_logger=main_logger,local_log=local_log)
        #self.pid = PID(self._set_engine_driver_values, depth_sensor_ref.get_depth, ahrs_ref, LOOP_DELAY)

    def set_lin_velocity(self, front, right, up):
        """
        Set linear velocity as 100% of engines power
        @param: front int in range [-100, 100], case negative value move back
        @param: right int in range [-100, 100], case negative value move down
        @param: up int in range [-100,100], case negative value move down
        """
        #self.pid.set_velocities(front, right, up)

    def set_ang_velocity(self, roll, pitch, yaw):
        """
        Set angular velocity as 100% of engines power
        @param: roll int in range [-100, 100], case negative - reverse direction
        @param: pitch int in range [-100, 100], case negative - reverse direction
        @param: yaw int in range [-100,100], case negative - reverse direction
        """
        #self.pid.set_velocities(yaw=yaw)

    def move_distance(self, front, right, up):
        """
        Make precise linear movement, valeues in meters
        @param: front float in range [-10, 10], case negative value move back
        @param: right float in range [-10, 10], case negative value move down
        @param: up float in range [-10,10], case negative value move down
        Not shure if it is going to work correctly
        """
        pass

    def rotate_angle(self, roll, pitch, yaw):
        """
        Make precise angular movement
        @param: roll float in range [-360, 360], case negative - reverse direction
        @param: pitch float in range [-360, 360], case negative - reverse direction
        @param: yaw flaot in range [-360, 360], case negative - reverse direction

        """
        pass

    def set_engine_driver_values(self, front, right, up, roll, pitch, yaw):
        self._send_data(self.to_dict(front, right, up, roll, pitch, yaw))
        print('Data sent')

    def to_dict(self, front=None, right=None, up=None, roll=None,
        pitch=None, yaw=None):
        '''
        Converting data to dictionary
        '''
        dic = {}
        for key,value in locals().items():
            if key != 'self' and key != 'dic' and value != None:
                dic[key] = value
        return dic

if __name__=='__main__':
    movements = Movements(None, None)
    print(movements.to_dict(12, 14, 15))
