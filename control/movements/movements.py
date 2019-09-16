"""

Module includes Movemnets clas
"""
import time
from math import copysign
from control.movements.movements_itf import IMovements
from control.pid.pid_depth import PIDdepth
from control.pid.pid_yaw import PIDyaw
from control.base_controller import BaseController

LOOP_DELAY = 0.05

# TODO - delete or move pyro server to communication (replace or integrate with communication for xavier)

class Movements(BaseController, IMovements):
    """
    Interfce for algorithm for accesing rpi Movement Class
    """
    def __init__(self, port, depth_sensor_ref, ahrs_ref, main_logger=None,
                 local_log=False, log_directory=""):
        """
        Construction of pid is like cascade:
        the pid_depth call the set_velocities method of the pid_yaw, so values doesn't get lost
        """
        super(Movements, self).__init__(port=port,
                                        main_logger=main_logger,
                                        local_log=local_log,
                                        log_directory=log_directory)
        self.pid_yaw = PIDyaw(self.send_values_to_engines,
                              ahrs_ref.get_yaw,
                              ahrs_ref,
                              LOOP_DELAY,
                              local_log=True,
                              log_directory=log_directory)
        # pid depth - master 
        self.pid_depth = PIDdepth(self.pid_yaw.set_velocities,
                                  depth_sensor_ref.get_depth,
                                  ahrs_ref,
                                  LOOP_DELAY,
                                  local_log=True,
                                  log_directory=log_directory)

        self.pid_depth.run()
        self.pid_yaw.run()
        self.ahrs = ahrs_ref
        self.get_depth = depth_sensor_ref.get_depth

    def set_lin_velocity(self, front, right, up):
        """
        Set linear velocity as 100% of engines power
        @param: front int in range [-100, 100], case negative value move back
        @param: right int in range [-100, 100], case negative value move down
        @param: up int in range [-100,100], case negative value move down
        """
        if up > 0.0001 or up < -0.0001:
            self.pid_depth_turn_off()
        else:
            self.pid_depth_turn_on() #TODO
        self.pid_depth.set_velocities(front/100, right/100, up/100)

        msg = "sset_lin vel: front: "+str(front)+";right: "+str(right)+";up: "+str(up)+";up: "+str(up)
        self.log(msg)

    def set_ang_velocity(self, roll, pitch, yaw):
        """
        Set angular velocity as 100% of engines power
        @param: roll int in range [-100, 100], case negative - reverse direction
        @param: pitch int in range [-100, 100], case negative - reverse direction
        @param: yaw int in range [-100,100], case negative - reverse direction
        """
        if yaw > 0.0001 or yaw < -0.0001:
            self.pid_yaw_turn_off()
        else:
            self.pid_yaw_turn_on()
        self.pid_depth.set_velocities(yaw=yaw/100)

    def move_distance(self, front, right, up):
        """
        Make precise linear movement, valeues in meters
        @param: front float in range [-10, 10], case negative value move back
        @param: right float in range [-10, 10], case negative value move down
        @param: up float in range [-10,10], case negative value move down
        Not shure if it is going to work correctly
        """
        print("move distance")
        ENIGNE_POWER = 25
        self.set_lin_velocity(ENIGNE_POWER*self.sign(front), 0, 0)
        if front<0:
            front = -front
        time.sleep(front*5)

        self.set_lin_velocity(0, ENIGNE_POWER*self.sign(right), 0)
        if right<0:
            right = -right
        time.sleep(right*5)

        self.set_lin_velocity(0, 0, 0)

        #self.pid_set_depth(self.get_depth()+up)


    def rotate_angle(self, roll, pitch, yaw):
        """
        Make precise angular movement
        @param: roll float in range [-180, 180], case negative - reverse direction
        @param: pitch float in range [-180, 180], case negative - reverse direction
        @param: yaw float in range [-180, 180], case negative - reverse direction

        """
        self.pid_set_yaw(self.ahrs.get_yaw()+yaw)

    def pid_hold_depth(self):
        self.pid_depth.hold_depth()
        self.log("movments: pid_hold_depth")

    def pid_depth_turn_on(self):
        #self.pid_hold_depth() #temporary
        self.pid_depth.turn_on_pid()
        self.log("movments: pid_turn_on")

    def pid_depth_turn_off(self):
        self.pid_depth.turn_off_pid()
        self.log("movments: pid_turn_off")

    def pid_depth_set_params(self, kp, ki, kd):
        self.pid_depth.set_pid_params(kp, ki, kd)
        self.log("movements: pid_set_params: kp: "+str(kp)+" ki: "+str(ki)+" kd: "+str(kd))

    def pid_set_depth(self, depth):
        """
        :param: depth - float - target depth for PID
        """
        self.pid_depth.set_depth(depth)
        self.log("set depth to "+str(depth))

    def pid_hold_yaw(self):
        self.pid_yaw.hold_yaw()
        self.log("movments: pid_hold_depth")

    def pid_yaw_turn_on(self):
        self.pid_hold_yaw() #temporary
        self.pid_yaw.turn_on_pid()
        self.log("movments: pid_turn_on")

    def pid_yaw_turn_off(self):
        self.pid_yaw.turn_off_pid()
        self.log("movments: pid_turn_off")

    def pid_yaw_set_params(self, kp, ki, kd):
        self.pid_yaw.set_pid_params(kp, ki, kd)
        self.log("movements: pid_set_params: kp: "+str(kp)+" ki: "+str(ki)+" kd: "+str(kd))

    def pid_set_yaw(self, yaw):
        """
        :param: angle - float - target depth for PID
        """
        self.pid_yaw.set_yaw(yaw)

    # for GUI
    def pid_depth_get_error(self):
        return self.pid_depth.get_error()

    def pid_depth_get_output(self):
        return self.pid_depth.get_output()
    
    def pid_yaw_get_error(self):
        return self.pid_yaw.get_error()

    def pid_yaw_get_output(self):
        return self.pid_yaw.get_output()

    def get_depth_set_point(self):
        return self.pid_depth.get_set_point()

    def get_yaw_set_point(self):
        return self.pid_yaw.get_set_point()
    # end for GUI

    def set_engine_driver_values(self, front, right, up, roll, pitch, yaw):
        self.pid_depth.set_velocities(front, right, up, roll, pitch, yaw)
        #msg = "set velocities in pid front: "+str(front)+";right: "+str(right)+";up: "+str(up)+";roll: "+str(roll)
        #self.log(msg)

    def send_values_to_engines(self, front, right, up, roll, pitch, yaw):
        self._send_data(self.to_dict(front, right, up, roll, pitch, yaw))
        #msg = "data sended: front: "+str(front)+";right: "+str(right)+";up: "+str(up)+";yaw: "+str(yaw)
        #self.log(msg)

    def to_dict(self, front=None, right=None, up=None, roll=None, pitch=None, yaw=None):
        '''
        Converting data to dictionary
        '''
        dic = {}
        for key,value in locals().items():
            if key != 'self' and key != 'dic' and value != None:
                dic[key] = value
        return dic

    @staticmethod
    def sign(val):
        if val > 0:
            return 1
        elif val < 0:
            return -1
        return 0

if __name__=='__main__':
    movements = Movements(None,None, None)
    print(movements.to_dict(12, 14, 15))
