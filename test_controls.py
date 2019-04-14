from control.lights.lights import Lights
from control.manipulator.manipulator import Manipulator
from control.torpedoes.torpedoes import Torpedoes
from control.movements.movements import Movements

from communication.rpi_drivers import ports

#a = Lights(port = ports.LIGHTS_CLIENT_PORT)
#b = Manipulator(port = ports.MANIP_CLIENT_PORT)
#c = Torpedoes(port = ports.TORPEDO_CLIENT_PORT)
d = Movements(port = ports.ENGINE_SLAVE_PORT,depth_sensor_ref = None, ahrs_ref = None,
main_logger = None)

#a.power_lights(10)
#b.set_movements('1 param','2 param')
#c.fire()
#c.power_laser(10)
d._set_engine_driver_values(1,2,None,4,5,6)