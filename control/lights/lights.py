from control.lights.lights_itf import ILights
from control.base_controller import BaseController

class Lights(BaseController,ILights):

    def power_lights(self,power_supplied):
        self._send_data(power_supplied)
        print('Lights turned on')
    def getter2msg(self):
        pass