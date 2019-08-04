import rov_comm
import ports

data_template = {'power':0}

server = rov_comm.ZMQ_Server(data_template,
client_port = ports.LIGHTS_DRIVER_PORT,
driver_port = ports.LIGHTS_CLIENT_PORT)

server.run()
