"""
Module includes BaseSensor class
"""
import abc
from threading import Lock
from logpy import Logger
from control.base_controller import BaseController
import zmq
import ast


class BaseSensor(BaseController, metaclass=abc.ABCMeta):
    """
    All sensors in sensors directory shoud inherit after this class
    """
    def __init__(self,port,timeout=200, main_logger=None, local_log=False, log_directory="",
                 log_timing=0.5):
        """
        :param main_logger: reference to external logger
        :param local_log: create local file with logs
        :param log_directory: directory for file with local logs
        :patam
        """
        super().__init__(port=port,timeout=timeout,main_logger=main_logger, local_log=local_log, log_directory=log_directory)
        
        self.local_logger = Logger(filename=self.__class__.__name__.lower(),
                                   directory=log_directory,
                                   title=self.__class__.__name__,
                                   external_function=self.getter2msg,
                                   internal_logger_time=log_timing)
        
        self.local_logger_lock = Lock()
    '''
    @abc.abstractmethod
    def getter2msg(self):
        """
        Convert data from class's getter/geters to log message
        :return: string containing single log message
        """
        pass
    '''
    def get_data(self):
        try:
            self.socket.send(b"give")
            #print("Sending request...")
            message = self.socket.recv()
            message = message.decode("utf-8")
            if str(type(message)) =="<class 'dict'>":
                message = ast.literal_eval(message)
            #print("Received reply:", message)
            self.server_up = True
            return message
        except zmq.ZMQError:
            #print("Server_down...")
            self.server_up = False
        if self.server_up is False:
            self.reboot()
'''
    @staticmethod
    def multithread_method(function):
        """
        Wraper for use with multiple threads accessing them
        All method called by getter2msg should have this decorator
        """
        def wrapper(self, *args):
            with self.local_logger_lock:
                function(self, args)
        return wrapper
        #Dominik W. - please check if indents are ok
'''