from sensors.hydrophones.hydrophones_itf import IHydrophonesPair


class HydrophonesPair(IHydrophonesPair):
    '''
    Class to handle hydrophones signal and
    calculate angle
    '''
    #@IHydrophonesPair.multithread_method
    def get_angle(self):
        return self.get_data()

    def getter2msg(self):
        return str(self.get_data())