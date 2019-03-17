import Pyro4
import threading

@Pyro4.expose
class Communication(threading.Thread):
    '''
    This class is responsible of finding Pyro4 nameserver,
    registering itself in there and providing all methods
    what classes passed from main thread offer.
    '''
    def __init__(self,sensors_refs,rpi_address, main_logger=None, local_logger=False, log_directory=''):
        '''
        Starting new thread, starting Pyro4 server,
        finding Pyro4 nameserver, registering 'self' in the nameserver,
        running Pyro4 server loop
        '''
        self.main_logger = main_logger
        self.local_logger = local_logger
        self.log_directory = log_directory
        threading.Thread.__init__(self)
        self.refs = sensors_refs
        #sensor_refs is used to store references to all objects passed from main thread

        daemon = Pyro4.Daemon(str(rpi_address))

        try:
            name_server = Pyro4.locateNS()  #It's possible to pass NS IP address to locateNS() (as string)
            #Tries to find Pyro nameserver

        except Exception as err:
            main_logger.log("Most probably couldn't find name server "+err)

        try:
            name_server.register('RPI_communication',daemon.register(self))
            #Tries to register self object in Pyro4 nameserver as 'RPI_communication'

        except Exception as err:
            main_logger.log('Problem with communication '+err)

        #main_logger.log('Communication server set correctly')
        daemon.requestLoop()
        #Starting Pyro4 server loop
    """
    def take_depth(self):
        '''
        Method provides DepthSensor class get_depth() method to Pyro server
        '''
        logging(take_depth.__name__,' - called')
        return self.refs['DepthSensor'].get_depth()

    def take_front_distance(self):
        '''
        Method provides FrontDistSensor class get_front_distance() method to Pyro server
        '''
        logging(take_front_distance.__name__,' - called')
        return self.refs[].get_front_distance()

    def take_bottom_distance(self):
        '''
        Method provides BottomDistSensor class get_bottom_distance() method to Pyro server
        '''
        logging(take_bottom_distance.__name__,' - called')
        return self.refs[].get_bottom_distance()

    def take_hydrophones_angle(self):
        '''
        Method provides HydrophonesMatrix class get_hydrophones_angle() method to Pyro server
        '''
        logging(take_hydrophones_angle.__name__,' - called')
        return self.refs[].get_hydrophones_angle()

    def set_angles(self):
        '''
        Method provides Manipulator class set_angles() method to Pyro server
        '''

        logging(set_angles.__name__,' '+str(angles))        #angles is set_angles method future parameter(s)
        self.refs[].set_angles()

    def move_distance(self):
        '''
        Method provides Movements() class move_distance() method to Pyro server
        '''
        logging(move_distance.__name__,' '+str(distance))   #distance is move_distance future parameter
        self.refs[].move_distance()

    def set_velocity(self):
        '''
        Method provides Movements() class set_velocity() method to Pyro server
        '''
        logging(set_velocity.__name__,' '+str(velocity))    #velocity is set_velocity future parameter
        self.refs[].set_velocity()
    def logging(self,name,msg = ''):
        '''
        Method is used for logging class Communication methods calls
        '''
        if main_logger != None:
            main_logger.log(name + str(msg))
        if local_logger != False:
            local_logger.log(name + str(msg))
    """
    def movements(self,front,right,up,yaw,roll=0,pitch=0):
        '''
		Method for pad steering for tests.
		'''
        self.refs['Movements'].set_lin_velocity(front,right,up)
        self.refs['Movements'].set_ang_velocity(roll,pitch,yaw)
'''
TO DO:
Change refs[] values to dictionary keys in Communication class methods
(Like in the take_depth() method)
'''
