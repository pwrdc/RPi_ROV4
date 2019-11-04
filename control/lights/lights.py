from control.lights.lights_itf import ILights
from control.base_controller import BaseController

class Lights(BaseController,ILights):

    def power_lights(self,power_supplied):
        '''
        set brightnes of lights
        :param power_supplied: int in range 0-100,
            0 - means turn lights off
            100 - stet lights to maxiumum brightness
        '''
        power_supplied = str(power_supplied)
        self._send_data(power_supplied)
        self.log('Lights set to '+power_supplied)

    def turn_on(self):
        self.power_lights(100)
        self.log("LIghts turn on")

    def turn_off(self):
        self.power_lights(0)
        self.log("Lights turn off")

    def getter2msg(self):
        pass