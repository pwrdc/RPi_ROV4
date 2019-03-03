#import Pyro4

@Pyro4.expose
class Communication(threading.Thread):
    '''
    This class is responsible of finding Pyro4 nameserver,
    registering itself in there and providing all methods
    what classes passed from main thread offer.
    '''
    def __init__(self,sensors_refs):
        '''
        Starting new thread, starting Pyro4 server,
        finding Pyro4 nameserver, registering 'self' in the nameserver,
        running Pyro4 server loop
        '''
        threading.Thread.__init__(self)
        self.refs = sensors_refs
        #sensor_refs is used to store references to all objects passed from main thread

        daemon = Pyro4.Daemon("192.168.1.4")   #RPI IP ADDRESS

        try:
            name_server = Pyro4.locateNS()  #It's available to pass NS IP address to locateNS()
            #Tries to find Pyro nameserver

        except Exception as err:
            print("Most probably couldn't find name server. Error:",err)

        try:
            name_server.register('RPI_communication',daemon.register(self))
            #Tries to register self object in Pyro4 nameserver as 'RPI_communication'

        except Exception as err:
            print('Failed to register Communication class object. Error:'
                  ,err)

        print('Communication server set correctly')
        daemon.requestLoop()
        #Starting Pyro4 server loop

    def take_depth(self):
        '''
        Method provides DepthSensor class get_depth() method to Pyro server
        '''
        return self.refs['DepthSensor'].get_depth()

    def take_front_distance(self):
        '''
        Method provides FrontDistSensor class get_front_distance() method to Pyro server
        '''
        return self.refs[].get_front_distance()

    def take_bottom_distance(self):
        '''
        Method provides BottomDistSensor class get_bottom_distance() method to Pyro server
        '''
        return self.refs[].get_bottom_distance()

    def take_hydrophones_angle(self):
        '''
        Method provides HydrophonesMatrix class get_hydrophones_angle() method to Pyro server
        '''
        return self.refs[].get_hydrophones_angle()

    def set_angles(self):
        '''
        Method provides Manipulator class set_angles() method to Pyro server
        '''
        self.refs[].set_angles()

    def move_distance(self):
        '''
        Method provides Movements() class move_distance() method to Pyro server
        '''
        self.refs[].move_distance()

    def set_velocity(self):
        '''
        Method provides Movements() class set_velocity() method to Pyro server
        '''
        self.refs[].set_velocity()

'''
TO DO:
Change refs[] values to dictionary keys in Communication class methods
(Like in the take_depth() method)
'''