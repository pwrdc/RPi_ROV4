import rov_comm
import settings

server = rov_comm.ZMQ_Server(settings.engine_master_port, settings.engine_slave_port)

server.run()
