from sensors.depth.depth_itf import IDepthSensor


class DepthSensor(IDepthSensor):
    '''
    '''
    @IDepthSensor.multithread_method
    def get_depth(self):
        '''
        Get current depth
        :return: depth as single integer
        '''
        pass

    def getter2msg():
        return str(get_depth())
