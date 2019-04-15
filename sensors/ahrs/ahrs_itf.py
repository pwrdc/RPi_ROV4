"""
Module includes interface for ahrs
"""
import abc



class IAHRS():
    """
    Class for getting data from ahrs sensor
    """
    @abc.abstractmethod
    def get_rotation(self):
        """
        Get current roations of ROV as single dictionary

        :return: single integer which represent depth of ROV in cm
            keys: "yaw", "pitch", "roll"
        """
        pass

    def get_linear_accelerations(self):
        """
        Get current linear accelerations as single dictionary

        :return: dictionary with accelerations
            keys: "lineA_x", "lineA_y", "lineA_z"
        """
        pass

    def get_angular_accelerations(self):
        """
        Get current angular accelerations as single dictionary

        :return: dictionary with accelerations
            keys: "anularA_x", "angularA_y", "angularA_z"
        """
        pass

    def get_yaw(self):
        """
        Get current yaw value

        :return: float which contain yaw
        """
        pass

    def get_all_data(self):
        """
        Get all curent data from sensor as single dictionary

        :return: dictionary with rotation, linear and angular acceleration
            keys: "yaw", "pitch", "roll"
                keys: "lineA_x", "lineA_y", "lineA_z"
                keys: "anularA_x", "angularA_y", "angularA_z"
        """
        pass
