from sensors.distance.distance import DistanceSensor

a = DistanceSensor(port=5560,timeout=200,local_log=True)
print(a.get_front_distance())
