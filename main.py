from logpy.LogPy import Logger

from communication.communication import Communication

#Sensors imports
from communication.rpi_drivers import settings
from sensors.distance.distance import DistanceSensor
from sensors.hydrophones.hydrophones import HydrophonesPair
from sensors.depth.depth import DepthSensor
from sensors.ahrs.ahrs import AHRS

#Control imports
from control.movements.movements import Movements
'''
Main object (thread) provides all sensors objects
and passes them to new thread Communication.
Communication thread is responsible of handling
Pyro4 server and requests to it.

Communication class has its own methods to all features it handles.
It is backed by easier use of Communication class from Xavier level.
(You don't have to know key of each sensor in sensor references dictionary)

'''

#definitions
RPI_ADDRESS = '192.168.0.100'

class Main():
    '''
    Creates object of all sensor types, packs their references into
    a list. Creates Communication thread.
    '''
    def __init__(self):
        '''
        Creates and stores references of all slave objects.
        '''
        self.logger = Logger(filename='main',directory='',logtype='info',timestamp='%Y-%m-%d | %H:%M:%S.%f',logformat='[{timestamp}] {logtype}:    {message}',prefix='',postfix='',title='Main Logger',logexists='append',console=False)
        
        self.ahrs = AHRS(port = settings.imu_client_port,main_logger = self.logger, local_log = True)
        self.depth = DepthSensor(port = settings.depth_client_port,
        main_logger = self.logger, local_log = True)
        self.hydrophones = HydrophonesPair(port =settings.hydro_client_port,
        main_logger = self.logger, local_log =True)
        self.distance = DistanceSensor(port = settings.distance_client_port,
        main_logger = self.logger, local_log = True)

        self.logger.start()

        self.depth.run()
        self.ahrs.run()
        self.hydrophones.run()
        self.distance.run()

        self.sensors_refs = {
            'AHRS':self.ahrs,
            'DepthSensor':self.depth,
            'HydrophonesPair':self.hydrophones,
            'DistanceSensor':self.distance
        }
        #Here you can add more feature classes
        #Remeber then to provide proper Communication class methods

        self.comm = Communication(self.sensors_refs, RPI_ADDRESS,
        main_logger = self.logger)
        '''
        Communication class parameters are: sensors_refs, rpi_address,
        main_logger, local_logger, log_directory (last three are optional)
        '''



if __name__== "__main__":
    main = Main()
    main.comm.start()
    main.comm.join()
    #Starting and waiting for infinite thread Communication to finish
