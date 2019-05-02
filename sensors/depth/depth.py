from sensors.depth.depth_itf import IDepthSensor
from sensors.base_sensor import BaseSensor


class DepthSensor(BaseSensor,IDepthSensor):
    '''
    Depth sensor
    Use rpi server to accessing data from sensor
    '''
    #@IDepthSensor.multithread_method
    def get_depth(self):
        '''
        Get current depth
        :return: depth as single integer
        '''
        return self.get_data()

    def getter2msg(self):
        #TODO this is temporary solution change to str(self.get_depth())
        return str(self.get_data())

