import rov_comm
import settings

server = rov_comm.ZMQ_Server(data_template=0,
driver_port = settings.distance_driver_port,
client_port = settings.distance_client_port)

server.run()