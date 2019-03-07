"""
Module includes BaseSensor class
"""
import abc
from threading import Thread, Lock
from time import sleep
from control.base_controller import BaseController


class BaseSensor(BaseController, metaclass=abc.ABCMeta):
    """
    All sensors in sensors directory shoud inherit after this class
    """
    def __init__(self, main_logger=None, local_log=False, log_directory="",
                 log_timing=0.5):
        """
        :param main_logger: reference to external logger
        :param local_log: create local file with logs
        :param log_directory: directory for file with local logs
        :patam
        """
        super().__init__(main_logger, local_log, log_directory)

        self.log_timing = log_timing
        self.close_sensor_logger = False
        self.close_sensor_logger_lock = Lock()
        # reference for thread with logging loop
        self.local_logger_loop_thread = None

    def run(self):
        """
        This method is called by main thread to start
        all additional threads for sensor's object
        If class does not need separate thread,
        implement this method with pass

        In case of sensor logging - place for start logging thread

        !! call parent's run method in case of override !!
        """
        if self.main_logger or self.local_logger:
            self.run_sensor_logger()

    def close(self):
        """
        This method is called by main thread to close
        all additional threads for sensor's object
        and related activities
        If class does not need to close separate thread,
        implement this method with pass

        !! call parent's close method in case of override !!
        """
        if self.main_logger or self.local_logger:
            self.stop_sensor_logger()

    def run_sensor_logger(self):
        """
        Run local logger
        """
        self.local_logger_loop_thread = Thread(target=self.get_sensor_log)
        self.local_logger_loop_thread.start()

    def stop_sensor_logger(self):
        """
        Stop local logger loop
        """
        with self.close_sensor_logger_lock:
            self.close_sensor_logger = True

    def get_sensor_log(self):
        """
        Loop which sends logs to local an main logger
        at inverts of time specified by log_timing
        by using getter2msg methods
        """
        self.close_sensor_logger_lock.acquire()
        while not self.close_sensor_logger:
            self.close_sensor_logger_lock.release()

            if self.main_logger:
                self.main_logger.log(self.getter2msg())

            if self.local_logger:
                self.local_logger.log(self.getter2msg())

            sleep(self.log_timing)
            self.close_sensor_logger_lock.acquire()

        self.local_logger.exit()

    @abc.abstractmethod
    def getter2msg(self):
        """
        Convert data from class's getter/geters to log message
        :return: string containing single log message
        """
        pass
