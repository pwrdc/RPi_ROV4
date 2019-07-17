import Pyro4
import threading

#Controls interfaces imports for inheritance
from control.lights.lights_itf import ILights
from control.manipulator.manipulator_itf import IManipulator
from control.movements.movements_itf import IMovements
from control.torpedoes.torpedoes_itf import ITorpedoes

#Sensors interfaces imports for inheritance
from sensors.ahrs.ahrs_itf import IAHRS
from sensors.depth.depth_itf import IDepthSensor
from sensors.distance.distance_itf import IDistanceSensor
from sensors.hydrophones.hydrophones_itf import IHydrophonesPair

@Pyro4.expose
class Communication(threading.Thread, ILights, IManipulator, IMovements,
                    ITorpedoes, IAHRS, IDepthSensor, IDistanceSensor, IHydrophonesPair):
    '''
    This class is responsible of finding Pyro4 nameserver,
    registering itself in there and providing all methods
    what classes passed from main thread offer.
    '''
    def __init__(self, sensors_refs, rpi_address, main_logger=None, log_directory=''):
        '''
        Starting new thread, starting Pyro4 server,
        finding Pyro4 nameserver, registering 'self' in the nameserver,
        running Pyro4 server loop
        '''
        self.main_logger = main_logger
        self.log_directory = log_directory
        threading.Thread.__init__(self)
        self.sensors_refs = sensors_refs

        #sensor_refs is used to store references to all objects passed from main thread

        daemon = Pyro4.Daemon(str(rpi_address))

        try:
            name_server = Pyro4.locateNS()  #It's possible to pass NS IP address to locateNS() (as string)
            #Tries to find Pyro nameserver

        except Exception as err:
            main_logger.log("Most probably couldn't find name server "+str(err))

        try:
            name_server.register('RPI_communication',daemon.register(self))
            #Tries to register self object in Pyro4 nameserver as 'RPI_communication'
            print('RPI registered in Pyro')

        except Exception as err:
            main_logger.log('Problem with communication '+str(err))

        main_logger.log('Communication server set correctly')
        daemon.requestLoop()
        #Starting Pyro4 server loop

    def power_lights(self, power_supplied):
        self.sensors_refs['Lights'].power_lights(power_supplied)

    # Movements
    def set_lin_velocity(self, front, right, up):
        self.sensors_refs['Movements'].set_lin_velocity(
            front, right, up
        )

    def set_ang_velocity(self, roll, pitch, yaw):
        self.sensors_refs['Movements'].set_ang_velocity(
            roll, pitch, yaw
        )

    def move_distance(self, front, right, up):
        self.sensors_refs['Movements'].move_distance(
            front, right, up
        )

    def rotate_angle(self, roll, pitch, yaw):
        self.sensors_refs['Movements'].rotate_angle(
            roll, pitch, yaw
        )

    def set_engine_driver_values(self, front, right, up,
                                 roll, pitch, yaw):
        self.sensors_refs['Movements'].set_engine_driver_values(
            front, right, up, roll, pitch, yaw
        )

    # Movements pid - depth
    def pid_depth_turn_on(self):
        self.sensors_refs['Movements'].pid_depth_turn_on()

    def pid_depth_turn_off(self):
        self.sensors_refs['Movements'].pid_depth_turn_off()

    def pid_hold_depth(self):
        self.sensors_refs['Movements'].pid_hold_depth()

    def pid_depth_set_params(self, kp, ki, kd):
        self.sensors_refs['Movements'].pid_depth_set_params(kp, ki, kd)

    def pid_set_depth(self, depth):
        """
        :param: depth - float - target depth for PID
        """
        self.sensors_refs['Movements'].pid_set_depth(depth)

    # Movements pid - yaw
    def pid_yaw_turn_on(self):
        self.sensors_refs['Movements'].pid_yaw_turn_on()

    def pid_yaw_turn_off(self):
        self.sensors_refs['Movements'].pid_yaw_turn_off()

    def pid_hold_yaw(self):
        self.sensors_refs['Movements'].pid_hold_yaw()

    def pid_yaw_set_params(self, kp, ki, kd):
        self.sensors_refs['Movements'].pid_yaw_set_params(kp, ki, kd)

    def pid_set_yaw(self, yaw):
        """
        :param: yaw - float in range [-180,180] - target yaw for PID
        """
        self.sensors_refs['Movements'].set_yaw(yaw)

    # Torpedoes
    def is_torpedo_ready(self):
        return self.sensors_refs['Torpedoes'].is_torpedo_ready()

    def torpedoe_fire(self):
        self.sensors_refs['Torpedoes'].fire()

    # Manipulator
    def set_movements(self, first_param, second_param):
        self.sensors_refs['Manipulator'].set_movements(first_param, second_param)

    def mainipulator_close_gripper(self):
        self.sensors_refs['Manipulator'].close_gripper()

    def mainipulator_open_gripper(self):
        self.sensors_refs['Manipulator'].open_gripper()

    # AHRS
    def get_rotation(self):
        return self.sensors_refs['AHRS'].get_rotation()

    def get_linear_accelerations(self):
        return self.sensors_refs['AHRS'].get_linear_accelerations()

    def get_angular_accelerations(self):
        return self.sensors_refs['AHRS'].get_angular_accelerations()

    def get_all_data(self):
        return self.sensors_refs['AHRS'].get_all_data()

    # Depth
    def get_depth(self):
        return self.sensors_refs['DepthSensor'].get_depth()

    # Distance
    def get_front_distance(self):
        return self.sensors_refs['DistanceSensor'].get_front_distance()

    # Hydrophones
    def get_angle(self):
        return self.sensors_refs['HydrophonesPair'].get_angle()
