from sensors.distance.distance_itf import IDistanceSensor
from sensors.base_sensor import BaseSensor

class DistanceSensor(BaseSensor,IDistanceSensor):
    '''
    '''
    #@IDistanceSensor.multithread_method
    def get_front_distance(self):
        '''
        Get distance from obstacle in front of ROV

        :return: distance as single integer
        '''
        return self.get_data()
    def getter2msg(self):
        return str(self.get_data())