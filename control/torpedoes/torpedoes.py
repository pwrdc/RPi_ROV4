from control.torpedoes.torpedoes_itf import ITorpedoes

class Torpedoes(ITorpedoes):
    def is_torpedo_ready(self):
        pass

    def fire(self):
        self._send_data('Fire')

    def power_laser(self, power_supplied):
        self._send_data(power_supplied)

    def getter2msg(self):
        pass 