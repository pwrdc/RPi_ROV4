from control.torpedoes.torpedoes_itf import ITorpedoes
from control.base_controller import BaseController

class Torpedoes(BaseController,ITorpedoes):
    def is_torpedo_ready(self):
        pass

    def fire_torpedo(self):
        self._send_data('Fire')

    def getter2msg(self):
        pass 