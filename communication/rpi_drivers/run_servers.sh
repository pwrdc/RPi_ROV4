!/bin/bash
python3.6 -m Pyro4.naming -n 192.168.0.102 &
python3.6 movements_server.py &
python3.6 ahrs_server.py &
python3.6 depth_server.py &
