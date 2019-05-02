"""
Module includes BaseSensor class
"""
import zmq
import ast
import abc
from logpy import Logger
from control.base_controller import BaseController


class BaseSensor(BaseController, metaclass=abc.ABCMeta):
    """
    All sensors in sensors directory shoud inherit after this class
    """
    def __init__(self, port, timeout=200, main_logger=None,
                 local_log=False, log_directory='', log_timing=0.5):
        super(BaseSensor, self).__init__(port=port,
                                         main_logger=main_logger,
                                         local_log=False,
                                         log_directory=log_directory)

        if local_log:
            self.local_logger = Logger(filename=self.__class__.__name__.lower(),
                                       directory=log_directory,
                                       title=self.__class__.__name__,
                                       external_function=self.getter2msg,
                                       internal_logger_time=log_timing)

    def get_data(self):
        try:
            self.socket.send(b"give")
            #Sending request...
            message = self.socket.recv()
            message = message.decode("utf-8")
            if message[0] == '{':
                message = ast.literal_eval(message)
            self.server_up = True
            return message
        except zmq.ZMQError:
            print("Server_down...")
            self.server_up = False
        if self.server_up is False:
            self.reboot()

    @abc.abstractmethod
    def getter2msg(self):
        """
        Convert data from class's getter/geters to log message
        :return: string containing single log message
        """
        pass
