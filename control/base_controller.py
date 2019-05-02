"""
Module includes BaseController class
"""
from control.base import Base
import zmq

class BaseController(Base):
    """
    All controllers in sensors directory should inherit from this class
    """
    def __init__(self, port, timeout=200, main_logger=None,
                 local_log=False, log_directory=''):
        """
        :param port: port for zmq client server communication
        :param timeout: recommended 2 times bigger than server timeout
        :param main_logger: reference to external logger
        :param local_log: create local file with logs
        :param log_directory: directory for file with local logs
        """
        super(BaseController, self).__init__(main_logger, local_log, log_directory)
        self.server_up = False
        self.connection_on = False
        self.port = port
        self.timeout =timeout
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO, self.timeout)
        self.socket.connect("tcp://localhost:" + str(self.port))
        self.connection_on = True
    
    def reboot(self):
        print("rebooting",self)
        self.context = zmq.Context()
        print("Trying to reconnect…")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO, self.timeout)
        self.socket.connect("tcp://localhost:" + str(self.port))

    def _send_data(self,data):
        try:
            self.socket.send(bytes(str(data), 'utf-8'))
            message = self.socket.recv()  # zmq.NOBLOCK)
            self.server_up = True
        except zmq.ZMQError:
            self.server_up = False
            self.log("serwer Down", 'error')
        if self.server_up is False:
            self.reboot()
