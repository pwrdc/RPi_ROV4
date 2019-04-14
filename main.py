from logpy.LogPy import Logger

from communication.communication import Communication

#Sensors imports
from communication.rpi_drivers import ports
from sensors.distance.distance import DistanceSensor
from sensors.hydrophones.hydrophones import HydrophonesPair
from sensors.depth.depth import DepthSensor
from sensors.ahrs.ahrs import AHRS

#Control imports
from control.movements.movements import Movements
from control.lights.lights import Lights
from control.manipulator.manipulator import Manipulator
from control.torpedoes.torpedoes import Torpedoes
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
RPI_ADDRESS = '192.168.0.190'
#orginally 192.168.0.100

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
        
        """
        #Sensors initialization
        self.ahrs = AHRS(port = ports.AHRS_CLIENT_PORT,main_logger = self.logger, local_log = True)
        self.depth = DepthSensor(port = ports.DEPTH_CLIENT_PORT,
        main_logger = self.logger, local_log = True)
        self.hydrophones = HydrophonesPair(port =ports.HYDRO_CLIENT_PORT,
        main_logger = self.logger, local_log =True)
        self.distance = DistanceSensor(port = ports.DISTANCE_CLIENT_PORT,
        main_logger = self.logger, local_log = True)

        #Controls initialization
        self.movements = Movements(port = ports.ENGINE_SLAVE_PORT,
        depth_sensor_ref = self.depth, ahrs_ref = self.ahrs, main_logger = self.logger)
        """
        self.lights = Lights (port = ports.LIGHTS_CLIENT_PORT,
        main_logger = self.logger)
        """
        self.manipulator = Manipulator(port = ports.MANIP_CLIENT_PORT,
        main_logger = self.logger)
        self.torpedoes = Torpedoes(port = ports.TORPEDO_CLIENT_PORT,main_logger=self.logger)
        #controls don't have to be run if they don't start local loggers

        self.logger.start()

        self.depth.run()
        self.ahrs.run()
        self.hydrophones.run()
        self.distance.run()
        """
        self.sensors_refs = {
            #'AHRS':self.ahrs,
            #'DepthSensor':self.depth,
            #'HydrophonesPair':self.hydrophones,
            #'DistanceSensor':self.distance,
            #'Movements':self.movements,
            'Lights':self.lights,
            #'Manipulator':self.manipulator,
            #'Torpedoes':self.torpedoes
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
