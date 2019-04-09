"""

Module includes Movemnets clas
"""
from communication.rpi_drivers.rov_comm import Client
import communication.rpi_drivers.settings
from control.movements.movements_itf import IMovements





# TODO - delete or move pyro server to communication (replace or integrate with communication for xavier)

class Movements(IMovements):

    """

    Interfce for algorithm for accesing rpi Movement Class

    """
    def __init__(self):
        super.__init__
        self.client = Client(movement_client_port)
    def set_lin_velocity(self, front, right, up):

        """

        Set linear velocity as 100% of engines power

        @param: front int in range [-100, 100], case negative value move back

        @param: right int in range [-100, 100], case negative value move down

        @param: up int in range [-100,100], case negative value move down

        """
        self.client.send_data(to_dict(front=front,
        right=right,up=up))
        



    def set_ang_velocity(self, roll, pitch, yaw):

        """

        Set angular velocity as 100% of engines power

        @param: roll int in range [-100, 100], case negative - reverse direction

        @param: pitch int in range [-100, 100], case negative - reverse direction

        @param: yaw int in range [-100,100], case negative - reverse direction

        """
        self.client.send_data(to_dict(roll=roll,
        pitch=pitch,yaw=yaw))

        #print("Angular velocity:",roll,pitch,yaw)



    def move_distance(self, front, right, up):

        """

        Make precise linear movement, valeues in meters

        @param: front float in range [-10, 10], case negative value move back

        @param: right float in range [-10, 10], case negative value move down

        @param: up float in range [-10,10], case negative value move down

        Not shure if it is going to work correctly

        """

        pass



    def rotate_angle(self, roll, pitch, yaw):

        """

        Make precise angular movement

        @param: roll float in range [-360, 360], case negative - reverse direction

        @param: pitch float in range [-360, 360], case negative - reverse direction

        @param: yaw flaot in range [-360, 360], case negative - reverse direction

        """

        pass

    def to_dict(self, front=None,right=None,up=None,roll=None
    ,pitch=None,yaw=None):
    '''
    Converting data to dictionary
    '''
        dic = locals()
        for i in dic:
            if i == None:
                del i
        return dic