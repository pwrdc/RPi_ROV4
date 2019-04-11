"""
Module includes BaseSensor class
"""

from control.base_controller import BaseController
import zmq
import ast
import abc


class BaseSensor(BaseController, metaclass=abc.ABCMeta):
    """
    All sensors in sensors directory shoud inherit after this class
    """
    
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
