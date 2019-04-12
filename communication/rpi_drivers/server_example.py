import rov_comm
import datetime

CLIENT_PORT = 1234
DRIVER_PORT = 1235

server = rov_comm.ZMQ_Server(data_template=0, client_port=CLIENT_PORT, driver_port=DRIVER_PORT)

server.run()
