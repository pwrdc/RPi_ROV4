import rov_comm
import datetime
import settings

server = rov_comm.ZMQ_Server(settings.imu_driver_port, settings.imu_client_port)

server.run()