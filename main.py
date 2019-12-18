'''
Main object (thread) provides all sensors objects
and passes them to new thread Communication.
Communication thread is responsible of handling
Pyro4 server and requests to it.

Communication class has its own methods to all features it handles.
It is backed by easier use of Communication class from Xavier level.
(You don't have to know key of each sensor in sensor references dictionary)

'''
from logpy.LogPy import Logger
import threading
from communication.communication import Communication

#Sensors imports
from communication.rpi_drivers import ports
from sensors.distance.distance import DistanceSensor
from sensors.hydrophones.hydrophones import HydrophonesPair
from sensors.depth.depth import DepthSensor
from sensors.ahrs.ahrs import AHRS
from inertial_navigation import InertialNavigation

#Control imports
from control.movements.movements import Movements
from control.lights.lights import Lights
from control.manipulator.manipulator import Manipulator
from control.torpedoes.torpedoes import Torpedoes
from control.dropper.dropper import Dropper

from definitions import MODE, DEFLOG, SENSORS, CONTROL, RPI_ADDRESS, INERTIAL_NAVIGATION


class Main():
    '''
    Creates object of all sensor types, packs their references into
    a list. Creates Communication thread.
    '''
    def __init__(self):
        '''
        Creates and stores references of all slave objects.
        '''
        self.logger = Logger(filename='main', title="Main", directory=DEFLOG.LOG_DIRECTORY)

        #Sensors initialization
        self.ahrs = None
        self.depth = None
        self.hydrophones = None
        self.distance = None
        self.inertial_navigation = None

        
        if SENSORS.AHRS:
            self.ahrs = AHRS(port=ports.AHRS_CLIENT_PORT,
                             main_logger=self.logger,
                             local_log=DEFLOG.AHRS_LOCAL_LOG,
                             log_timing=DEFLOG.AHRS_LOG_TIMING,
                             log_directory=DEFLOG.LOG_DIRECTORY,
                             mode=MODE)
        
        if SENSORS.DEPTH:
            self.depth = DepthSensor(port=ports.DEPTH_CLIENT_PORT,
                                     main_logger=self.logger,
                                     local_log=DEFLOG.DEPTH_LOCAL_LOG,
                                     log_timing=DEFLOG.DEPTH_LOG_TIMING,
                                     log_directory=DEFLOG.LOG_DIRECTORY)
        if SENSORS.HYDROPHONES:
            self.hydrophones = HydrophonesPair(port=ports.HYDRO_CLIENT_PORT,
                                               main_logger=self.logger,
                                               local_log=DEFLOG.HYDROPHONES_LOCAL_LOG,
                                               log_timing=DEFLOG.HYDROPHONES_LOG_TIMING,
                                               log_directory=DEFLOG.LOG_DIRECTORY)
        if SENSORS.DISTANCE:
            self.distance = DistanceSensor(port=ports.DISTANCE_CLIENT_PORT,
                                           main_logger=self.logger,
                                           local_log=DEFLOG.DISTANCE_LOCAL_LOG,
                                           log_timing=DEFLOG.HYDROPHONES_LOG_TIMING,
                                           log_directory=DEFLOG.LOG_DIRECTORY)

        #Controls initialization
        self.lights = None
        self.manipulator = None
        self.torpedoes = None
        self.dropper = None
        self.movements = Movements(port=ports.ENGINE_SLAVE_PORT,
                                   depth_sensor_ref=self.depth,
                                   ahrs_ref=self.ahrs,
                                   main_logger=self.logger,
                                   local_log=DEFLOG.MOVEMENTS_LOCAL_LOG,
                                   log_directory=DEFLOG.LOG_DIRECTORY)
        if CONTROL.LIGHTS:
            self.lights = Lights(port=ports.LIGHTS_CLIENT_PORT, main_logger=self.logger)
        if CONTROL.MANIPULATOR:
            self.manipulator = Manipulator(port=ports.MANIP_CLIENT_PORT, main_logger=self.logger)
        if CONTROL.TORPEDOES:
            self.torpedoes = Torpedoes(fire_client_port=ports.TORPEDO_FIRE_CLIENT_PORT,
                                       ready_driver_port=ports.TORPEDO_READY_DRIVER_PORT,
                                       main_logger=self.logger,
                                       local_log=DEFLOG.TORPEDOES_LOCAL_LOG,
                                       log_directory=DEFLOG.LOG_DIRECTORY)
        if CONTROL.DROPPER:
            self.dropper = Dropper(self.logger)

        

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
            'Torpedoes':self.torpedoes,
            'dropper':self.dropper
        }        


        #Here you can add more feature classes
        #Remeber then to provide proper Communication class methods


        if SENSORS.INERTIAL_NAVIGATION:
            self.inertial_navigation = InertialNavigation(INERTIAL_NAVIGATION.INITIAL_STATE,
                                                          self.ahrs,
                                                          INERTIAL_NAVIGATION.IS_ORIENTATION_SIMPLIFIED)

        if SENSORS.INERTIAL_NAVIGATION:
            self.inertial_navigation.run()


        self.comm = Communication(self.sensors_refs, RPI_ADDRESS, main_logger=self.logger)
        '''
        Communication class parameters are: sensors_refs, rpi_address,
        main_logger, local_logger, log_directory (last three are optional)
        '''

        

if __name__== "__main__":
    main = Main()
    main.comm.start()
    main.comm.join()
    #St
