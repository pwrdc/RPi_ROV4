!/bin/bash
python3 -m Pyro4.naming -n 192.168.0.102 &
python3 movements_server.py &
python3 ahrs_server.py &
python3 depth_server.py &
