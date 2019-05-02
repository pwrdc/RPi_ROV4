import rov_comm
import ports

example ={
    'front':0,
    'right':0,
    'up':0,
    'roll':0,
    'pitch':0,
    'yaw':0
}
server = rov_comm.ZMQ_Server(example, ports.ENGINE_SLAVE_PORT, ports.ENGINE_MASTER_PORT)

server.run()
