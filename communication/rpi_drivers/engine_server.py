import rov_comm
import settings

example ={
    'front':0,
    'right':0,
    'up':0,
    'roll':0,
    'pitch':0,
    'yaw':0
}
server = rov_comm.ZMQ_Server(example,settings.engine_master_port, settings.engine_slave_port)

server.run()
