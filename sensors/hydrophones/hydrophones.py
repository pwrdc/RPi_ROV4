from sensors.hydrophones.hydrophones_itf import IHydrophonesPair
from sensors.base_sensor import BaseSensor

class HydrophonesPair(BaseSensor,IHydrophonesPair):
    '''
    Class to handle hydrophones signal and
    calculate angle
    '''
    #@Base.multithread_method
    def get_angle(self):
        return self.get_data()

    def getter2msg(self):
        return str(self.get_data())