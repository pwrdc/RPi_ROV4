"""
Separate test for sensors ZMQ communication
"""
from sensors.distance.distance import DistanceSensor
from sensors.depth.depth import DepthSensor
from sensors.ahrs.ahrs import AHRS
from sensors.hydrophones.hydrophones import HydrophonesPair

from communication.rpi_drivers import ports



#a = DistanceSensor(port=ports.DISTANCE_CLIENT_PORT,timeout=200,local_log=False)
#b = DepthSensor(port=ports.DEPTH_CLIENT_PORT,timeout=200,local_log=False)
c = AHRS(port=ports.AHRS_CLIENT_PORT, timeout=200, local_log=False)
#d = HydrophonesPair(port=ports.HYDRO_CLIENT_PORT, timeout =200, local_log = False)




#print('Distance Sensor response',a.get_front_distance())

#print('Depth Sensor response',b.get_depth())

print('AHRS response',c.get_angular_accelerations())
print('AHRS response',c.get_linear_accelerations())
print('AHRS response',c.get_rotation())
print('AHRS response',c.getter2msg())

#print('Hydrophones response',d.getter2msg())

#To test run needed servers from /communication/rpi_drivers/
#then run particular sensor here