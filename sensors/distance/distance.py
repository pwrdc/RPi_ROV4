from sensors.distance.distance_itf import IDistanceSensor
#from distance_itf import IDistanceSensor

class DistanceSensor(IDistanceSensor):
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
        pass
