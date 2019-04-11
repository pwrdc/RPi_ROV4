"""
Module includes BaseSensor class
"""
from logpy import Logger
import zmq
import ast

class BaseController():
    """
    All controllers in sensors directory should inherit from this class
    """
    def __init__(self,port,timeout, main_logger=None, local_log=False, log_directory=""):
        """
        :param port: port for zmq client server communication
        :param timeout: recommended 2 times bigger than server timeout
        :param main_logger: reference to external logger
        :param local_log: create local file with logs
        :param log_directory: directory for file with local logs
        """
        self.server_up = False
        self.connection_on = False
        self.port = port
        self.timeout =timeout
        self.context = zmq.Context()
        self.main_logger = main_logger
        self.local_logger = None
        if local_log:
            self.local_logger = Logger(filename=self.__class__.__name__.lower(),
                                       directory=log_directory,
                                       title=self.__class__.__name__)
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO, self.timeout)
        self.socket.connect("tcp://localhost:" + str(self.port))
        self.connection_on = True
    
    def reboot(self):
        print("rebooting")
        self.context = zmq.Context()
        print("Trying to reconnect…")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO, self.timeout)
        self.socket.connect("tcp://localhost:" + str(self.port))

    def run(self):
        """
        This method is called by main thread to start
        all additional threads for sensor's object
        If class does not need separate thread,
        implement this method with pass

        In case of sensor logging - place for start logging thread
        !! call parent's run method in case of override !!
        """
        if self.local_logger:
            self.local_logger.start()

    def close(self):
        """
        This method is called by main thread to close
        all additional threads for sensor's object
        and related activities
        If class does not need to close separate thread,
        implement this method with pass
        """
        if self.local_logger:
            self.local_logger.exit()

    def log(self, msg, logtype=''):
        """
        Send log to main and local logger

        :param msg: string which contain message for log
        :param logtype: message logtype, log type; available:
            'info', 'warning', 'error', 'fatal'
        """
        if self.main_logger:
            self.main_logger.log(msg, logtype)

        if self.local_logger:
            self.local_logger.log(msg, logtype)
