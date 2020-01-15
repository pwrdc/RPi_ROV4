# TODO replace direct ahrs connection with server

from sensors.ahrs.ahrs_itf import IAHRS
from sensors.base_sensor import BaseSensor
import ast
import struct
import threading
import time
import serial
import os
from logpy.LogPy import Logger
import math
IMU_PORT = '/dev/ttyUSB0'

"""
from sensors.ahrs.ahrs_separate import AHRS_Separate
from sensors.ahrs.ahrs_virtual import AHRSvirtual
from threading import Thread
"""


class AHRS(BaseSensor, IAHRS):
    '''
    class for accessing AHRS data using direct access to ahrs thread
    If AHRS is disconected use virtual class to returning only zeros

    '''
    def __init__(self, port, timeout=200, main_logger=None, local_log=False,
                 log_directory='', log_timing=0.5, mode="ROV4"):
        super(AHRS, self).__init__(port=port,
                                   timeout=timeout,
                                   main_logger=main_logger,
                                   local_log=local_log,
                                   log_directory=log_directory,
                                   log_timing=log_timing)
        self.mode = mode
        if mode != 'SIMULATION':
            self.ahrs = AHRS_Separate(log_directory)
        self.thread = threading.Thread(target=self.ahrs.run)
        self.thread.start()

    def get_data(self):
        return self.ahrs.get_data()

    def getter2msg(self):
        return str(self.get_yaw())

    def get_yaw(self):
        """
        :return: yaw - float walue,
        value takes into account multiple rotations
        possible values in whole range of real numbers
        """
        if self.mode == 'SIMULATION':
            received = self.get_data()
            return received['yaw']
        else:
            return self.ahrs.yaw + self.ahrs.yaw_correction

    #@Base.multithread_method
    def get_rotation(self):
        '''
        :return: dict with keys: 'yaw', 'pitch', 'roll'
        '''
        if self.mode == 'SIMULATION':
            received = self.get_data()
            output = {}
            if received != None:
                #received = ast.literal_eval(received)
                output['yaw'] = received['yaw']
                output['pitch'] = received['pitch']
                output['roll'] = received['roll']
                return output
            else:
                return None
        else:
            dictionary = {'yaw': self.ahrs.yaw, 'pitch': self.ahrs.pitch,
                          'roll': self.ahrs.roll}
            return dictionary

    #@Base.multithread_method
    def get_linear_accelerations(self):
        '''
        :return: dictionary with keys "lineA_x"
        "lineA_y", lineA_z"
        '''
        if self.mode == 'SIMULATION':
            received = self.get_data()
            output = {}
            print(received)
            if received != None:
                #received = ast.literal_eval(received)
                output['lineA_x'] = received['lineA_x']
                output['lineA_y'] = received['lineA_y']
                output['lineA_z'] = received['lineA_z']
                return output
            else:
                return None
        else:
            return {'lineA_x': self.ahrs.free_acc[0],
                    'lineA_y': self.ahrs.free_acc[1],
                    'lineA_z': self.ahrs.free_acc[2]}

    #@Base.multithread_method
    def get_angular_accelerations(self):
        '''
        :return: dictionary with keys "angularA_x"
        "angularA_y", angularA_z"
        '''
        if self.mode == 'SIMULATION':
            received = self.get_data()
            output = {}
            print(received)
            if received != None:
                #received = ast.literal_eval(received.decode("utf-8"))
                output['angularA_x'] = received['angularA_x']
                output['angularA_y'] = received['angularA_x']
                output['angularA_z'] = received['angularA_x']
                return output
            else:
                return None
        else:
            return {"angularA_x": self.ahrs.rate_of_turn[0],
                    "angularA_y": self.ahrs.rate_of_turn[1],
                    "angularA_z": self.ahrs.rate_of_turn[2]}

    #@Base.multithread_method
    def get_time(self):
        '''
        :return: dictionary with keys "time"
        '''
        if self.mode == 'SIMULATION':
            received = self.get_data()
            output = {}
            print(received)
            if received != None:
                #received = ast.literal_eval(received.decode("utf-8"))
                output['time'] = received['time']
                return output
            else:
                return None
        else:
            return {"time": float(self.ahrs.timestamp)/10000}

    #@Base.multithread_method
    def get_all_data(self):
        '''
        :return: dictionary with rotation, linear and angular
        accelerations, keys: "yaw", "pitch", "roll",
        "lineA_x","lineA_y","lineA_z","angularA_x",
        "angularA_y","angularA_z"
        '''
        if self.mode == 'SIMULATION':
            return self.get_data()
        else:
            rot = self.get_rotation()
            lin_acc = self.get_linear_accelerations()
            ang_acc = self.get_angular_accelerations()
            return {**rot, **lin_acc, **ang_acc}

    #@Base.multithread_method
    def get_inertial_navigation_data(self):
        '''
        :return: dictionary with time, rotation in radians
        and linear accelerations,
        keys: "time",
        "yaw", "pitch", "roll",
        "lineA_x", "lineA_y", "lineA_z"
        '''
        if self.mode == 'SIMULATION':
            data = self.get_data()
        else:
            time = self.get_time()
            print(time)
            rot = self.get_rotation()
            lin_acc = self.get_linear_accelerations()
            # degrees to radians
            keys = ["yaw", "pitch", "roll"]
            for key in keys:
                rot[key] = math.radians(rot[key])
            data = {**time, **rot, **lin_acc}
        return data




class BytesQueue:
    def __init__(self, buffer: bytes):
        self.data = buffer

    def pop(self, size=1):
        x = self.data[:size]
        self.data = self.data[size:]

        if size > 1:
            return x
        else:
            return x[0]

    def length(self):
        return len(self.data)


class AHRS_Separate():
    timestamp = 0
    yaw = 0
    pitch = 0
    roll = 0
    free_acc = [0, 0, 0]
    rate_of_turn = [0, 0, 0]

    def __init__(self, log_direcory=""):
        self.serial = serial.Serial(IMU_PORT, 115200, stopbits=2, parity=serial.PARITY_NONE)
        self.lock_timestamp = threading.Lock()
        self.lock_rate_of_turn = threading.Lock()
        self.lock_free_acc = threading.Lock()
        self.lock_angular_pos = threading.Lock()
        self.logger = Logger(filename='ahrs_separate', directory=log_direcory, logtype='info',
                             logformat='[{timestamp}] {logtype}:    {message}',
                             title='AHRS logger', logexists='append', console=False) 
        self.close_order = False

        self.yaw_correction = 0.0
        self.previous_yaw = 0.0

    def get_message(self):
        MID = 0
        data = 0
        ser = self.serial

        while True:
            pre = ser.read()
            if pre.hex() == 'fa':  # check preamble
                bid = ser.read()
                checksum = bid[0]
                if bid.hex() == 'ff':  # check bus ID
                    MID = ser.read(1)[0]
                    checksum += MID
                    len = ser.read()
                    len_value = len[0]

                    checksum += len_value

                    if len.hex() == 'ff':  # extended message
                        len_ext = ser.read(2)
                        len_value = int.from_bytes(len_ext, 'big')
                        checksum += len_ext[0] + len_ext[1]

                    data = ser.read(len_value)

                    for byte in data:
                        checksum += byte

                    checksum += ser.read()[0]

                    if checksum & 0xff == 0:  # Checksum OK!
                        break

        self._interpret_message(MID, data)

        self.should_fix()

    def _interpret_euler(self, data: BytesQueue):
        length = data.pop()
        if length != 12:
            print("Unexpected euler angles data length")

        roll_bytes = data.pop(4)
        pitch_bytes = data.pop(4)
        yaw_bytes = data.pop(4)

        with self.lock_angular_pos:
            self.roll = struct.unpack(">f", roll_bytes)[0]
            self.pitch = struct.unpack(">f", pitch_bytes)[0]
            self.yaw = struct.unpack(">f", yaw_bytes)[0]

    def _interpret_free_acceleration(self, data: BytesQueue):
        length = data.pop()
        if length != 12:
            print("Unexpected free acceleration data length")

        accX_bytes = data.pop(4)
        accY_bytes = data.pop(4)
        accZ_bytes = data.pop(4)

        with self.lock_free_acc:
            self.free_acc[0] = struct.unpack(">f", accX_bytes)[0]
            self.free_acc[1] = struct.unpack(">f", accY_bytes)[0]
            self.free_acc[2] = struct.unpack(">f", accZ_bytes)[0]

    def _interpret_rate_of_turn(self, data: BytesQueue):
        length = data.pop()
        if length != 12:
            print("Unexpected rate of turn data length")

        rotX_bytes = data.pop(4)
        rotY_bytes = data.pop(4)
        rotZ_bytes = data.pop(4)

        with self.lock_rate_of_turn:
            self.rate_of_turn[0] = struct.unpack(">f", rotX_bytes)[0]
            self.rate_of_turn[1] = struct.unpack(">f", rotY_bytes)[0]
            self.rate_of_turn[2] = struct.unpack(">f", rotZ_bytes)[0]

    def _interpret_mtdata2(self, data: BytesQueue):
        while data.length() > 0:
            data_type = data.pop(2)
            if data_type.hex() == "1060":
                self._interpret_timestamp(data)
            elif data_type.hex() == "2030":
                self._interpret_euler(data)
            elif data_type.hex() == "4030":
                self._interpret_free_acceleration(data)
            elif data_type.hex() == "8020":
                self._interpret_rate_of_turn(data)
            else:
                # print("Unexpected mtdata2 information type: {hex}".format(hex=data_type.hex()))
                return

    def _interpret_timestamp(self, data: BytesQueue):
        length = data.pop()
        if length != 4:
            print("Unexpected timestamp data length")
        sampleTimeFine_bytes = data.pop(4)

        with self.lock_timestamp:
            self.timestamp = struct.unpack(">I", sampleTimeFine_bytes)[0]

    def _interpret_message(self, mid: int, data: bytes):
        data_queue = BytesQueue(data)

        if mid == 0x36:
            self._interpret_mtdata2(data_queue)
        else:
            print("WARNING: Unknown message type")

    def get_data(self):
        """
        To call from oudstide the function
        :return: {'lineA_x':0,'lineA_y':0,'lineA_z':0, 'angularA_x':0,'angularA_y':0,'angularA_z':0, 'yaw':0,'pitch':0,'roll':0}
        """
        data = {}
        with self.lock_free_acc:
            data['lineA_x'] = (self.free_acc[0])
            data['lineA_y'] = (self.free_acc[1])
            data['lineA_z'] = (self.free_acc[2])
        with self.lock_angular_pos:
            data['yaw'] = (self.yaw)
            data['pitch'] = (self.pitch)
            data['roll'] = (self.roll)
        with self.lock_rate_of_turn:
            data['angularA_x'] = (self.rate_of_turn[0])
            data['angularA_y'] = (self.rate_of_turn[1])
            data['angularA_z'] = (self.rate_of_turn[2])

            data["time"] = time.time()
        return data

    def run(self):

        while not self.close_order:
            self.get_message()

    def close(self):
        self.close_order = True

    @staticmethod
    def isAHRSconected():
        '''
        :return: True if you can use AHRS or False if you can't
        '''
        return os.path.exists(IMU_PORT)

    def should_fix(self):
        LIMIT = 175.0
        if self.yaw > LIMIT and self.previous_yaw < -LIMIT:
            self.yaw_correction -= 360.0
        elif self.yaw  < -LIMIT and self.previous_yaw > LIMIT:
            self.yaw_correction += 360.0
        self.logger.log("prev: "+str(self.previous_yaw)+" curr: "+str(self.yaw))
        self.previous_yaw = self.yaw



if __name__ == "__main__":
    with serial.Serial(IMU_PORT, 115200, stopbits=2, parity=serial.PARITY_NONE) as serial_port:
        imu = AHRS_Separate()

        while True:
            imu.get_message()
            '''
            x=("Yaw: {yaw}; Pitch: {pitch}; Roll: {roll}\n".format(yaw=imu.yaw, pitch=imu.pitch,
                                                                    roll=imu.roll))  # rotacja - polozenie katowe
            y=("RotX: {rot0}; RotY: {rot1}; RotZ: {rot2}\n".format(rot0=imu.rate_of_turn[0], rot1=imu.rate_of_turn[1],
                                                                    rot2=imu.rate_of_turn[2]))
            z=("AccX: {facc0}; AccY: {facc1}; AccZ: {facc2}\n".format(facc0=imu.free_acc[0], facc1=imu.free_acc[1],
                                                                    facc2=imu.free_acc[2]))
            imu.logger.log(x+y+z,logtype='')
            '''
            print("Yaw: {yaw}; Pitch: {pitch}; Roll: {roll}".format(yaw=imu.yaw, pitch=imu.pitch,
                                                                    roll=imu.roll))  # rotacja - polozenie katowe
            print("RotX: {rot0}; RotY: {rot1}; RotZ: {rot2}".format(rot0=imu.rate_of_turn[0], rot1=imu.rate_of_turn[1],
                                                                    rot2=imu.rate_of_turn[2]))
            print("AccX: {facc0}; AccY: {facc1}; AccZ: {facc2}".format(facc0=imu.free_acc[0], facc1=imu.free_acc[1],
                                                                       facc2=imu.free_acc[2]))
            print("----------------------------------")
