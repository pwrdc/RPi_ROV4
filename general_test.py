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

cmd = "self.sensors_refs['{}'].{}"

try:
    Pyro4.locateNS()
    RPI = Pyro4.Proxy("PYRONAME:RPI_communication")
except Exception as err:
    print (err)

try:
    print(RPI)
    RPI.do(cmd.format('Lights','power_lights(10)'))
    #RPI.refs['AHRS'].get_all_data()     this won't work due to serialization problem
except Exception as err:
    print(err)