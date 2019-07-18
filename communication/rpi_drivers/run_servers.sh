#!/bin/bash
python3 -m Pyro4.naming -n 192.168.0.100 &
python3 movements_server.py &
python3 ahrs_server.py &
python3 depth_server.py &
python3 distance_server.py &
#python3 manipulator_server.py &
#python3 torpedo_server.py &

