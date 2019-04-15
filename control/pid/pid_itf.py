from threading import Thread
import abc

class IPID():
    @abc.abstractclassmethod
    def set_velocities(self, front=None, right=None, up=None, yaw=None):
        """
        Program turn off depth controll if up != None and set velocities diretly
        Set angular velocity as % of engines power
        :param front: float in range [-1, 1], case negative value move back
        :param right: float in range [-1, 1], case negative value move down
        :param up: float in range [-1,1], case negative value move down
        :param yaw: float in range [-1,1], case negative - reverse direction
        """
        pass

    @abc.abstractclassmethod
    def hold_depth(self):
        '''
        Program remember current ROV depth and hold it
        '''
        pass

    @abc.abstractclassmethod
    def set_depth(self, depth):
        '''
        Set angular velocity as 100% of engines power
        :param depth: integer - target depth of ROV in cm
        '''
        pass
