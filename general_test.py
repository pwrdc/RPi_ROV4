"""
Simple Pyro4 cliento to test all
RPI functionalities.

Instruction:
1. run Pyro4 nameserver python3 -m Pyro4.naming -n IP_ADDRESS
2. run all servers from /communication/rpi_drivers
(on Windows you can only run run_all_servers.bat)
3. run main.py
4. run this script
"""
import Pyro4
import time

cmd = "self.sensors_refs['{}'].{}"

try:
    Pyro4.locateNS()
    RPI = Pyro4.Proxy("PYRONAME:RPI_communication")
except Exception as err:
    print (err)

try:
    print(RPI)
    RPI.power_lights(10)
    print('After power lights')
    time.sleep(1)
    RPI.set_movements(1,2)
    print('After set movements')
    time.sleep(1)
    RPI.set_lin_velocity(3,4,5)
    print('After set lin vel')
    time.sleep(1)
    RPI.set_ang_velocity(7,8,9)
    print('After set ang vel')
    time.sleep(1)
    RPI.move_distance(1,1,1)
    print('after move dist')
    time.sleep(1)
    RPI.rotate_angle(2,2,2)
    print('After rot angle')
    time.sleep(1)
    RPI.set_engine_driver_values(1,2,3,4,5,6)
    print('after set eng values')
    time.sleep(1)
    print(RPI.is_torpedo_ready())
    print('after is torpedo redy')
    time.sleep(1)
    RPI.fire()
    print('after fire')
    time.sleep(1)
    RPI.power_laser(5)
    print('after power laser')
    time.sleep(1)
    print(RPI.get_rotation(),'rotation')
    print('after get rotati')
    time.sleep(1)
    print(RPI.get_linear_accelerations(),'linear acc')
    print('after get lin acc')
    time.sleep(1)
    print(RPI.get_angular_accelerations(),'ang acc')
    print('after get ang acc')
    time.sleep(1)
    print(RPI.get_all_data(),'all data')
    print('after get all data')
    time.sleep(1)
    print(RPI.get_depth(),'depth')
    print('after get depth')
    time.sleep(1)
    print(RPI.get_front_distance(),'front')
    print('after get fr dist')
    time.sleep(1)
    print(RPI.get_angle(),'hydro')
    print('after get angle')
    #RPI.refs['AHRS'].get_all_data()     this won't work due to serialization problem
except Exception as err:
    print(err)