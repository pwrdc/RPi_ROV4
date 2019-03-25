from sensors.depth.depth_itf import IDepthSensor
from communication.rpi_drivers.rov_comm import Client
from communication.rpi_drivers.settings import depth_client_port


class DepthSensor(IDepthSensor):
    '''
    Depth sensor
    Use rpi server to accessing data from sensor
    '''
    def __init__(self, main_logger=None, local_log=False, log_directory="", log_timing=0.5):
        super().__init__(main_logger, local_log, log_directory, log_timing)
        self.client = Client(depth_client_port)

    @IDepthSensor.multithread_method
    def get_depth(self):
        '''
        Get current depth
        :return: depth as single integer
        '''
        return self.client.get_data()

    def getter2msg(self):
        return str(self.get_depth())
