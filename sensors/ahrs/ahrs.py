from sensors.ahrs.ahrs_itf import IAHRS


class AHRS(IAHRS):
    '''
    '''
    @IAHRS.multithread_method
    def get_rotation(self):
        '''
        '''
        pass

    @IAHRS.multithread_method
    def get_linear_accelerations(self):
        '''
        :return: dictionary with keys "lineA_x"
        "lineA_y", lineA_z"
        '''
        pass

    @IAHRS.multithread_method
    def get_angular_accelerations(self):
        '''
        :return: dictionary with keys "angularA_x"
        "angularA_y", angularA_z"
        '''
        pass

    @IAHRS.multithread_method
    def get_all_data(self):
        '''
        :return: dictionary with rotation, linear and angular
        accelerations, keys: "yaw", "pitch", "roll",
        "lineA_x","lineA_y","lineA_z","angularA_x",
        "angularA_y","angularA_z"
        '''
        pass
