import rov_comm
import datetime
import settings

driver = rov_comm.Client(settings.imu_driver_port)
client = rov_comm.Client(settings.imu_client_port)

if not (driver.connection_on is True and client.connection_on is True):
    print("server down")
else:
    while True:
        driver.send_data(datetime.datetime.now().time())
        data = client.get_data()
        print(data)

print("Goodbye")

