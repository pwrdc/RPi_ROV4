from control.lights.lights_itf import ILights

class Lights(ILights):

    def power_lights(self,power_supplied):
        self._send_data(power_supplied)
        print(power_supplied)
    def getter2msg(self):
        pass