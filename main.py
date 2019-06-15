from logpy.LogPy import Logger
import threading
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

from definitions import DEFLOG, SENSORS, CONTROL, RPI_ADDRESS
'''
Main object (thread) provides all sensors objects
and passes them to new thread Communication.
Communication thread is responsible of handling
Pyro4 server and requests to it.

Communication class has its own methods to all features it handles.
It is backed by easier use of Communication class from Xavier level.
(You don't have to know key of each sensor in sensor references dictionary)

'''


class Main():
    '''
    Creates object of all sensor types, packs their references into
    a list. Creates Communication thread.
    '''
    def __init__(self):
        '''
        Creates and stores references of all slave objects.
        '''
        self.logger = Logger(filename='main', title="Main")

        #Sensors initialization
        self.ahrs = None
        self.depth = None
        self.hydrophones = None
        self.distance = None
        if SENSORS.AHRS:
            self.ahrs = AHRS(
                             main_logger=self.logger,
                             local_log=DEFLOG.AHRS_LOCAL_LOG)
                             
        if SENSORS.DEPTH:
            self.depth = DepthSensor(
                                     main_logger=self.logger,
                                     local_log=DEFLOG.DEPTH_LOCAL_LOG)
        if SENSORS.HYDROPHONES:
            self.hydrophones = HydrophonesPair(port=ports.HYDRO_CLIENT_PORT,
                                               main_logger=self.logger,
                                               local_log=DEFLOG.HYDROPHONES_LOCAL_LOG,
                                               log_timing=DEFLOG.HYDROPHONES_LOG_TIMING)
        if SENSORS.DISTANCE:
            self.distance = DistanceSensor(port=ports.DISTANCE_CLIENT_PORT,
                                           main_logger=self.logger,
                                           local_log=DEFLOG.DISTANCE_LOCAL_LOG,
                                           log_timing=DEFLOG.HYDROPHONES_LOG_TIMING)

        #Controls initialization
        self.lights = None
        self.manipulator = None
        self.torpedoes = None
        self.movements = Movements(depth_sensor_ref=self.depth,
                                   ahrs_ref=self.ahrs,
                                   main_logger=self.logger,
                                   local_log=DEFLOG.MOVEMENTS_LOCAL_LOG)
        if CONTROL.LIGHTS:
            self.lights = Lights(port=ports.LIGHTS_CLIENT_PORT, main_logger=self.logger)
        if CONTROL.MANIPULATOR:
            self.manipulator = Manipulator(port=ports.MANIP_CLIENT_PORT, main_logger=self.logger)
        if CONTROL.TORPEDOES:
            self.torpedoes = Torpedoes(port=ports.TORPEDO_CLIENT_PORT, main_logger=self.logger)
        
        #Run threads, in control for local logers

        self.logger.start()
        if SENSORS.DEPTH:
            self.depth.run()
        if SENSORS.AHRS:
            self.ahrs.run()
        if SENSORS.HYDROPHONES:
            self.hydrophones.run()
        if SENSORS.DISTANCE:
            self.distance.run()

        self.movements.run()
        if CONTROL.MANIPULATOR:
            self.manipulator.run()
        if CONTROL.LIGHTS:
            self.manipulator.run()
        if CONTROL.TORPEDOES:
            self.torpedoes.run()
        
        self.sensors_refs = {
            'AHRS':self.ahrs,
            'DepthSensor':self.depth,
            'HydrophonesPair':self.hydrophones,
            'DistanceSensor':self.distance,
            'Movements':self.movements,
            'Lights':self.lights,
            'Manipulator':self.manipulator,
            'Torpedoes':self.torpedoes
        }
        #Here you can add more feature classes
        #Remeber then to provide proper Communication class methods

        self.comm = Communication(self.sensors_refs, RPI_ADDRESS, main_logger=self.logger)
        '''
        Communication class parameters are: sensors_refs, rpi_address,
        main_logger, local_logger, log_directory (last three are optional)
        '''



if __name__== "__main__":
    main = Main()
    main.comm.start()
    main.comm.set_lin_velocity(0,0,0,0)
    main.comm.set_lin_velocity(0,0,0,0)
    main.comm.set_lin_velocity(0,0,0,0)
    main.comm.join()
    #St
