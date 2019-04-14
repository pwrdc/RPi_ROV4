import Pyro4

try:
    Pyro4.locateNS()
    RPI = Pyro4.Proxy("PYRONAME:RPI_communication")
except Exception as err:
    print (err)

try:
    print(RPI)
    RPI.metoda()
    RPI.refs['Lights'].power_lights(10)
    #RPI.refs['AHRS'].get_all_data()
except Exception as err:
    print(err)