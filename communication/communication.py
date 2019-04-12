import Pyro4
import threading

@Pyro4.expose
class Communication(threading.Thread):
    '''
    This class is responsible of finding Pyro4 nameserver,
    registering itself in there and providing all methods
    what classes passed from main thread offer.
    '''
    def __init__(self,sensors_refs, rpi_address, main_logger=None, log_directory=''):
        '''
        Starting new thread, starting Pyro4 server,
        finding Pyro4 nameserver, registering 'self' in the nameserver,
        running Pyro4 server loop
        '''
        self.main_logger = main_logger
        self.log_directory = log_directory
        threading.Thread.__init__(self)
        self.refs = sensors_refs
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

        except Exception as err:
            main_logger.log('Problem with communication '+str(err))

        main_logger.log('Communication server set correctly')
        daemon.requestLoop()
        #Starting Pyro4 server loop

