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

    def set_lin_velocity(self, front, right, up):
        """
        Set linear velocity as 100% of engines power
        @param: front int in range [-100, 100], case negative value move back
        @param: right int in range [-100, 100], case negative value move down
        @param: up int in range [-100,100], case negative value move down
        """
        self.pid_depth.set_velocities(front/100, right/100, up/100)

    def set_ang_velocity(self, roll, pitch, yaw):
        """
        Set angular velocity as 100% of engines power
        @param: roll int in range [-100, 100], case negative - reverse direction
        @param: pitch int in range [-100, 100], case negative - reverse direction
        @param: yaw int in range [-100,100], case negative - reverse direction
        """
        self.pid_depth.set_velocities(yaw=yaw/100)

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
        @param: roll float in range [-180, 180], case negative - reverse direction
        @param: pitch float in range [-180, 180], case negative - reverse direction
        @param: yaw float in range [-180, 180], case negative - reverse direction

        """
        allowed_error = 5 # in degrees
        break_factor = 0.2 # greater value => faster speed down

        direction = copysign(1, yaw)
        dest_yaw = self.ahrs.get_rotation()["yaw"] + yaw
        break_angle = break_factor * yaw
        if abs(dest_yaw) > 180:
            dest_yaw -= copysign(360, dest_yaw)
        stop = False
        breaking = False
        while not stop:
            error = dest_yaw - self.ahrs.get_rotation()["yaw"]
            self.log("rotation: error "+str(error))
            if abs(error) > allowed_error:
                if not breaking and (abs(error) <= break_angle):
                    direction *= -1
                    breaking = True
                self.set_engine_driver_values(0, 0, 0, 0, 0, direction)
                self.log("val of rotation: "+str(direction))
                time.sleep(0.001)
            else:
                stop = True

    def pid_hold_depth(self):
        self.pid_depth.hold_depth()
        self.log("movments: pid_hold_depth")

    def pid_depth_turn_on(self):
        self.pid_hold_depth() #temporary
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
        msg = "data sended: front: "+str(front)+";right: "+str(right)+";up: "+str(up)+";yaw: "+str(yaw)
        self.log(msg)

    def to_dict(self, front=None, right=None, up=None, roll=None, pitch=None, yaw=None):
        '''
        Converting data to dictionary
        '''
        dic = {}
        for key,value in locals().items():
            if key != 'self' and key != 'dic' and value != None:
                dic[key] = value
        return dic

if __name__=='__main__':
    movements = Movements(None,None, None)
    print(movements.to_dict(12, 14, 15))
