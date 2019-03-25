from threading import Thread
from sensors.ahrs.ahrs_itf import IAHRS
#from sensors.ahrs.ahrs_separate import AHRS_Separate

import serial

class AHRS(IAHRS):
    '''
    '''
    def __init__(self, main_logger=None, local_log=False):
        #serial_port = serial.Serial('/dev/ttyUSB0', 115200, stopbits=2, parity=serial.PARITY_NONE)
        super().__init__(main_logger,local_log)
        #self.ahrs = AHRS_Separate(serial_port)

    def run(self):
        super().run()
        thread = Thread(target=self.ahrs.run, name="ahrs separate thread")
        thread.run()

    def close(self):
        super.close()
        self.ahrs.close()
        
    def getter2msg(self):
        return str(self.ahrs.get_data())
		
    @IAHRS.multithread_method
    def get_rotation(self):
        '''
        :return: dict with keys: 'yaw', 'pitch', 'roll' 
        '''
        received = self.ahrs.get_data()
        output = {}

        output['yaw'] =  received['yaw']
        output['pitch'] = received['pitch']
        output['roll'] = received['roll']

    @IAHRS.multithread_method
    def get_linear_accelerations(self):
        '''
        :return: dictionary with keys "lineA_x"
        "lineA_y", lineA_z"
        '''
        received = self.ahrs.get_data()
        output = {}

        output['lineA_x'] = received['lineA_x']
        output['lineA_y'] = received['lineA_y']
        output['lineA_z'] = received['lineA_z']

    @IAHRS.multithread_method
    def get_angular_accelerations(self):
        '''
        :return: dictionary with keys "angularA_x"
        "angularA_y", angularA_z"
        '''
        received = self.ahrs.get_data()
        output = {}

        output['angularA_x'] = received['angularA_x']
        output['angularA_y'] = received['angularA_x']
        output['angularA_z'] = received['angularA_x']

    @IAHRS.multithread_method
    def get_all_data(self):
        '''
        :return: dictionary with rotation, linear and angular
        accelerations, keys: "yaw", "pitch", "roll",
        "lineA_x","lineA_y","lineA_z","angularA_x",
        "angularA_y","angularA_z"
        '''
        received = self.ahrs.get_data()
        output = {}

        output['lineA_x'] = received['lineA_x']
        output['lineA_y'] = received['lineA_y']
        output['lineA_z'] = received['lineA_z']

        output['yaw'] =  received['yaw']
        output['pitch'] = received['pitch']
        output['roll'] = received['roll']

        output['angularA_x'] = received['angularA_x']
        output['angularA_y'] = received['angularA_x']
        output['angularA_z'] = received['angularA_x']

