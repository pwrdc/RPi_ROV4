import time

from control.movements.settings import depth_driver_port, depth_client_port
from control.movements.rov_comm import Client, ZMQ_Server

if __name__ == '__main__':
    
    server = ZMQ_Server(depth_driver_port, depth_client_port)
    server.run()
    client = Client(depth_driver_port)
    loop_condition = True
    while loop_condition:
        client.send_data(12.5)

        time.sleep(1)

    # in case of sensor error
