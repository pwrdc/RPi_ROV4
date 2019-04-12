import rov_comm
import settings

server = rov_comm.ZMQ_Server(data_template=0,
driver_port = settings.hydro_driver_port,
client_port = settings.hydro_client_port)

server.run()