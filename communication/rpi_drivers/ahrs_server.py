import rov_comm
import settings

data_temp = {
    'lineA_x':0,
    'lineA_y':0,
    'lineA_z':0,
    'angularA_x':0,
    'angularA_y':0,
    'angularA_z':0,
    'roll':0,
    'pitch':0,
    'yaw':0
}
server = rov_comm.ZMQ_Server(data_template=data_temp,
driver_port = settings.imu_driver_port,
client_port = settings.imu_client_port)

server.run()