from control.torpedoes.torpedoes_itf import ITorpedoes
from control.base_controller import Base
from communication.rpi_drivers import rov_comm, ports
import time

class Torpedoes(Base, ITorpedoes):

    def __init__(self, fire_client_port, ready_driver_port, main_logger=None, local_log=False, log_directory=""):
        """
        Construction of pid is like cascade:
        the pid_depth call the set_velocities method of the pid_yaw, so values doesn't get lost
        """
        super(Torpedoes, self).__init__(main_logger=main_logger,
                                        local_log=local_log,
                                        log_directory=log_directory)
        self.client_fire = rov_comm.Client(fire_client_port)
        self.client_ready = rov_comm.Client(ready_driver_port)

    def is_torpedo_ready(self):
        if self.client_ready.get_data() == 'READY':
            return True
        else:
            return False

    def fire_torpedo(self):
        self.log("torpedo fired")
        self.client_fire.send_data('FIRE')
        while self.is_torpedo_ready():
            pass
        self.log("reoloaded")
        self.client_fire.send_data('HOLD')

    def getter2msg(self):
        pass

if __name__ == "__main__":
    obrotowa = Torpedoes()
    while True:
        obrotowa.fire_torpedo()
        time.sleep(1)