from sensors.depth.depth_itf import IDepthSensor
from sensors.base_sensor import BaseSensor
import time
from threading import Thread

class DepthSensor(BaseSensor, IDepthSensor):
    '''
    Depth sensor
    Use rpi server to accessing data from sensor
    '''
    def __init__(self, port, timeout=200, main_logger=None,
                 local_log=False, log_directory='', log_timing=0.5):
        super(DepthSensor, self).__init__(port=port,
                                          timeout=timeout,
                                          main_logger=main_logger,
                                          local_log=local_log,
                                          log_directory=log_directory,
                                          log_timing=log_timing)
        self.depth = 0.0
        self.thread = Thread(target=self.fun)
        self.thread.start()

    #@BaseSensor.multithread_method
    def get_depth(self):
        '''
        Get current depth
        :return: depth as single integer
        '''
        #TODO sometime returning None when to ofen ask for data
        #current_depth = self.get_data()
        #if current_depth:
        #    self.depth = current_depth
        return self.depth

    def fun(self):
        while True:
            current_depth = self.get_data()
            if current_depth:
                self.depth = float(current_depth)
            time.sleep(0.01)

    def getter2msg(self):
        return str(self.get_depth())
