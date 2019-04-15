from control.pid.pid_itf import IPID
from threading import Thread
from control.base import Base

class PID(Base,IPID):
    def __init__(self, set_engine_driver_fun, get_depth_fun, ahrs, loop_delay, 
        main_logger=None, local_log=False, log_directory="",log_timing=0.5):
        '''
        Set linear velocity as 100% of engines power
        @param set_engine_driver_fun: reference to _set_engine_driver_values
                in Movements object (see movments_itf.py)
        @param get_depth_fun: reference to method returning depth
                (see get_depth in sensor/depth/depth_itf.py)
        @param ahrs: reference to AHRS object
                (see AHRS in sensors/ahrs/ahrs_itf.py)
        '''
        super(Base,self).__init__(main_logger, local_log, log_directory,log_timing)
        self.set_engine_driver_fun = set_engine_driver_fun
        self.get_depth_fun = get_depth_fun
        self.ahrs = ahrs
        self.loop_delay = loop_delay

    def run(self):
        super().run()
        thread = Thread(target=self.pid_loop) # TODO replace pid_loop with your local method with main loop
        thread.run()
