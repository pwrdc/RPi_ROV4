import time
from threading import Thread, Lock
from control.base import Base
from control.pid.pid_itf import IPID
from definitions import PID_YAW as PID_DEF

UP_MARGIN = 0.04


class PIDyaw(Base, IPID):
    def __init__(self,
                 set_engine_driver_fun,
                 get_yaw_fun,
                 ahrs,
                 loop_delay,
                 main_logger=None,
                 local_log=False,
                 log_directory="",
                 pid_loop_run_allowed=False,
                 kp=PID_DEF.KP,
                 ki=PID_DEF.KI,
                 kd=PID_DEF.KD):
        '''
        Set linear velocity as 100% of engines power
        :param set_engine_driver_fun: reference to _set_engine_driver_values
                in Movements object (see movments_itf.py)
        :param get_yaw_fun: reference to method returning yaw
        :param ahrs: reference to AHRS object
                (see AHRS in sensors/ahrs/ahrs_itf.py)
        :param pid_loop_active: boolean value - if true pid loop activates in run()
        '''
        super(PIDyaw, self).__init__(main_logger, local_log, log_directory)

        self.set_point = 0.0

        self.front = 0.0
        self.right = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0

        self.set_engine_driver_fun = set_engine_driver_fun
        self.get_yaw_fun = get_yaw_fun
        self.ahrs = ahrs
        self.sample_time = loop_delay
        self.pid_loop_lock = Lock()
        self.pid_active_lock = Lock()
        self.pid_active = False
        self.get_yaw_fun_lock = Lock()

        self.pid_loop_run_allowed = pid_loop_run_allowed

        self.close_bool = False

        self.current_time = time.time()
        self.last_time = self.current_time
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd

        self.clear()

    def get_yaw(self):
        with self.get_yaw_fun_lock:
            return self.get_yaw_fun()

    def clear(self):
        '''
        Clears all PID variables and set_point.
        '''
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.int_error = 0.0
        self.windup_guard = 1.0
        self.output = 0.0

    def update(self, feedback_value):
        '''
        Calculate PID for given feedback.
        Result is stored in PID.output.
        '''
        error = (self.set_point - feedback_value)

        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            self.last_time = self.current_time
            self.last_error = error

            self.output = (self.PTerm + (self.Ki * self.ITerm) + (
                self.Kd * self.DTerm))
        self.log("Output update; error: "+ str(error)+ "  output: " +str(self.output))

    def run(self):
        self.log("PID: running")
        super().run()
        if self.pid_loop_run_allowed:
            thread = Thread(target=self.pid_loop)
            thread.start()
            self.log("PID: finish running")

    def close(self):
        super().close()
        with self.pid_loop_lock:
            self.close_bool = True

    def hold_yaw(self):
        """
        set current yaw of vehicle as target for PID
        """
        self.set_point = self.get_yaw()
        self.log("hold yaw: "+ str(self.set_point))

    def set_yaw(self, yaw):
        """
        :param: yaw - float - target yaw for PID
        """
        self.set_point = yaw
        self.clear()

    def pid_loop(self):
        num = 0
        while True:
            time.sleep(self.sample_time)
            yaw = self.get_yaw()
            self.log('Get yaw ' + str(yaw))
            if yaw:
                self.update(float(yaw))
                with self.pid_loop_lock:
                    if self.close_bool:
                        break
                with self.pid_active_lock:
                    if self.pid_active:
                        num += 1
                        if num == 1:
                            num = 0
                            self.log("yaw pid kp= "+str(self.Kp)+" ki= "+str(self.Ki)+" kd= "+str(self.Kd)+str((self.front, self.right,
                                                                           self.up, self.roll, self.pitch, self.val_to_range(self.output))))
                        self.set_engine_driver_fun(self.front, self.right, self.up, self.roll, self.pitch, self.val_to_range(self.output))

    def turn_on_pid(self):
        with self.pid_active_lock:
            self.log("yaw PID activated")
            self.pid_active = True
            self.clear()
            self.log("yaw PID activated")

    def turn_off_pid(self):
        with self.pid_active_lock:
            self.log("yaw PID deactivated")
            self.pid_active = False

    def set_pid_params(self, kp, ki, kd):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        self.log("yaw pid_set_params: kp: "+str(kp)+" ki: "+str(ki)+" kd: "+str(kd))

    @staticmethod
    def val_to_range(val):
        if val < -1:
            return -1.0
        if val > 1:
            return 1.0
        return val

    def set_velocities(self, front=0, right=0, up=0, roll=0, pitch=0, yaw=0):
        self.front=front
        self.right=right
        self.roll=roll
        self.pitch=pitch
        self.up=up

        with self.pid_active_lock:
            if (up>UP_MARGIN and up < -UP_MARGIN) or not self.pid_active:
                self.set_engine_driver_fun(front, right, up, roll, pitch, yaw)
                #self.log("Send normal values")
            else:
                self.set_engine_driver_fun(front, right, up, roll, pitch, self.val_to_range(self.output))
