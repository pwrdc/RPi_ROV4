from sensors.depth.depth_itf import IDepthSensor
from control.base import Base
import Pyro4


class DepthSensor(Base,IDepthSensor):
    '''
    Depth sensor
    Use rpi server to accessing data from sensor
    '''
    #@IDepthSensor.multithread_method
    def __init__(self, main_logger=None, local_log=False):
        super(DepthSensor, self).__init__(main_logger=main_logger, local_log=local_log)
        Pyro4.locateNS()
        self.depth_server = Pyro4.Proxy("PYRONAME:depth_server")
    def get_depth(self):
        '''
        Get current depth
        :return: depth as single integer
        '''
        return self.depth_server.get_depth()

    def getter2msg(self):
        #TODO this is temporary solution change to str(self.get_depth())
        return str(self.depth_server.get_depth())

