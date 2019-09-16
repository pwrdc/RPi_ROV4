from sensors.distance.distance_itf import IDistanceSensor
from sensors.base_sensor import BaseSensor

class DistanceSensor(BaseSensor,IDistanceSensor):
    '''
    '''
    prev_val = 3500
    #@Base.multithread_method
    def get_front_distance(self):
        '''
        Get distance from obstacle in front of ROV

        :return: distance as single float
        '''
        print(self.prev_val)
        val = self.get_data()
        try:
            self.prev_val = val
            return float(self.get_data())
        except Exception:
            return self.prev_val

    def getter2msg(self):
        return str(self.get_data())