"""
File contains definitions of const values in code
"""
MODE = "ROV4"  # 'ROV3' or 'ROV4' or 'SIMULATION'

if MODE == 'SIMULATION':
    RPI_ADDRESS = '127.0.0.1'  # local address
else:
    RPI_ADDRESS = '192.168.0.105'  # RPi address

class DEFLOG:
    LOG_DIRECTORY = "logs/RPi/"

    INERTIAL_NAVIGATION_LOG = True
    INERTIAL_NAVIGATION_LOG_TIMING = 0.0025

    DEPTH_LOCAL_LOG = True
    DEPTH_LOG_TIMING = 0.1

    AHRS_LOCAL_LOG = True
    AHRS_LOG_TIMING = 0.1

    HYDROPHONES_LOCAL_LOG = False
    HYDROPHONES_LOG_TIMING = 0.1

    DISTANCE_LOCAL_LOG = True
    DISTANCE_LOG_TIMING = 0.1

    MOVEMENTS_LOCAL_LOG = True
    MANIPULATOR_LOCAL_LOG = False
    TORPEDOES_LOCAL_LOG = False

class SENSORS:
    INERTIAL_NAVIGATION = True
    AHRS = True
    DEPTH = True
    HYDROPHONES = False
    DISTANCE = False

class CONTROL:
    LIGHTS = False
    MANIPULATOR = False
    TORPEDOES = False
    DROPPER = False

class PID_DEPTH:
    if MODE == 'ROV4':
        # values for ROV4:
        KP = 2.44 #1.38
        KI = 0.012 #0.0192
        KD = 0.0913 #0.84
    elif MODE == 'ROV3':
        # values for ROV3:
        KP = 3.69
        KI = 0.0
        KD = 0.84

class PID_YAW:
    KP = 0.04 #0.0
    KI = 0.001#.0
    KD = 0.004#0.0

class INERTIAL_NAVIGATION:
    INITIAL_STATE = {"yaw": 0,
                     "pitch": 0,
                     "roll": 0,
                     "lineP_x": 0,
                     "lineP_y": 0,
                     "lineP_z": 0
                     }
    IS_ORIENTATION_SIMPLIFIED = False

    CONSTANT_BIAS = {"lineA_x": -0.00141857862271016,
                     "lineA_y": -0.0129980750314774,
                     "lineA_z": -0.0325809329152555
                     }
