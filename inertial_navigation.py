"""
TODO:
integracja (oczywiście)
obsługa przejścia przez końce zakresu dla yaw
przerzucić do głównego folderu
"""

import time

import numpy as np
from math import sin, cos, radians, pi
from communication.rpi_drivers import ports


class InertialNavigation():
    SLEEP_TIME = 0.002
    SKIPPED_SAMPLES = 10
    ACC_CUT_THRESHOLD = 0.1

    def __init__(self, initial_state, ahrs_ref, constant_bias, simplified_orientation=False,
                 simplified_displacement=False):
        print("inertial navigation - start")
        self.ahrs = ahrs_ref
        self.constant_bias = constant_bias
        self.simplified_orientation = simplified_orientation
        self.simplified_displacement = simplified_displacement

        # pomijanie pierwszych, niewłaściwych próbek
        self.skip_samples()

        # słownik wejściowy z ahrs z wartościami 0, poza time, który jest niezmieniony
        acc_sample_template = self.get_input_data()
        time_sample = acc_sample_template["time"]
        for key in acc_sample_template:
            acc_sample_template[key] = 0
        acc_sample_template["time"] = time_sample

        # zmiana kluczy słowników na odpowiadające danym
        keys_acc = ["lineA_x", "lineA_y", "lineA_z"]
        keys_vel = ["lineV_x", "lineV_y", "lineV_z"]
        keys_pos = ["lineP_x", "lineP_y", "lineP_z"]
        vel_sample_template = acc_sample_template.copy()
        for i in range(len(keys_acc)):
            del vel_sample_template[keys_acc[i]]
            vel_sample_template[keys_vel[i]] = 0
        pos_sample_template = acc_sample_template.copy()
        for i in range(len(keys_acc)):
            del pos_sample_template[keys_acc[i]]
            pos_sample_template[keys_pos[i]] = 0

        # próbki przyspieszeń, prędkości, przemieszczenia i pozycji
        # 0 - najnowsza próbka
        self.acc_samples = []
        for i in range(3):
            self.acc_samples.append(acc_sample_template.copy())

        self.vel_samples = []
        for i in range(2):
            self.vel_samples.append(vel_sample_template.copy())
        self.dis_sample = pos_sample_template.copy()
        self.pos_sample = pos_sample_template.copy()
        for key in initial_state:
            self.pos_sample[key] = initial_state[key]

        # przejście z zakresu [-pi, pi] do [0, 2pi]
        # (wymagane do obsługi get_global_displacement)
        #keys = ["yaw", "pitch", "roll"]
        #for key in keys:
        #    if self.pos_sample[key] < 0:
        #        self.pos_sample[key] += 2 * pi

        # do obrotu układu ahrs do układu z initial_state
        self.yaw_correction = self.get_input_data()["yaw"]
        #if self.yaw_correction < 0:
        #    self.yaw_correction += 2*pi

        self.file_log = open("inertial_navigation_log.csv", "w")
        self.file_log.write("time, yaw, pitch, roll, lineP_x, lineP_y, lineP_z\n")

        self.file_log_raw_data = open("inertial_navigation_log_raw_data.csv", "w")
        self.file_log_raw_data.write("time, yaw, pitch, roll, lineA_x, lineA_y, lineA_z\n")

    # powinno być wywoływane cyklicznie, dla każdej próbki z AHRS
    def run(self):
        while True:
            # przesunięcie próbek, dodanie nowej próbki z AHRS
            self.acc_samples[2] = self.acc_samples[1].copy()
            self.acc_samples[1] = self.acc_samples[0].copy()
            self.acc_samples[0] = self.get_input_data()
            self.vel_samples[1] = self.vel_samples[0].copy()

            # pobranie orientacji prosto z ahrs, bez przeliczania z przyspieszeń
            keys = ["yaw", "pitch", "roll"]
            for key in keys:
                self.dis_sample[key] = self.acc_samples[0][key]

            # obrót z układu ahrs do układu z initial state
            self.dis_sample["yaw"] -= self.yaw_correction

            # przejście z zakresu [-pi, pi] do [0, 2pi]
            # (wymagane do obsługi get_global_displacement)
            #for key in keys:
            #    if self.dis_sample[key] <= 0:
            #        self.dis_sample[key] += 2*pi

            # przemieszczenie w lokalnym układzie współrzędnych
            self.get_internal_displacement()

            # przeniesienie lokalnych przemieszczeń na układ globalny
            self.get_global_displacement()

            # dodanie przemieszczeń do poprzedniej pozycji
            self.get_global_coordinates()

            #return self.pos_sample
            msg = ""
            for key in self.pos_sample:
                msg += str(self.pos_sample[key]) + ", "
            msg += "\n"
            self.file_log.write(msg)
            msg = ""
            for key in self.acc_samples[0]:
                msg += str(self.acc_samples[0][key]) + ", "
            msg += "\n"
            self.file_log_raw_data.write(msg)
            time.sleep(self.SLEEP_TIME)

    # przemieszczenie we współrzędnych wewnętrznych
    def get_internal_displacement(self):
        self.vel_samples[0]["time"] = self.acc_samples[0]["time"]
        # obliczenia dla wszystkich kierunków
        keys_acc = ["lineA_x", "lineA_y", "lineA_z"]
        keys_vel = ["lineV_x", "lineV_y", "lineV_z"]
        keys_pos = ["lineP_x", "lineP_y", "lineP_z"]
        for i in range(len(keys_acc)):
            # całkowanie numeryczne metodą trapezów
            d_time = self.acc_samples[0]["time"] - self.acc_samples[1]["time"]
            if d_time > 1:
                d_time = 0.0025
                print("time error")
            self.vel_samples[0][keys_vel[i]] += 0.5 * (
                        self.acc_samples[0][keys_acc[i]] + self.acc_samples[1][keys_acc[i]]) * d_time
            d_time = self.vel_samples[0]["time"] - self.vel_samples[1]["time"]
            if d_time > 1:
                d_time = 0.0025
            self.dis_sample[keys_pos[i]] = 0.5 * (
                        self.vel_samples[0][keys_vel[i]] + self.vel_samples[1][keys_vel[i]]) * d_time

    # przemieszczenie we współrzędnych globalnych
    def get_global_displacement(self):
        if self.simplified_displacement:
            yaw = self.dis_sample["yaw"]
            pitch = self.dis_sample["pitch"]
            roll = self.dis_sample["roll"]
        else:
            # obroty o kąt początkowy + połowa zmiany kąta ( = średnia kątów z dwóch kolejnych próbek)
            # to nie jest żadne przybliżenie tylko dokładna wartość. i mogę to udowodnić!
            yaw = (self.pos_sample["yaw"] + self.dis_sample["yaw"]) / 2
            pitch = (self.pos_sample["pitch"] + self.dis_sample["pitch"]) / 2
            roll = (self.pos_sample["roll"] + self.dis_sample["roll"]) / 2
        dis_sample_matrix_local = np.array(
            [[self.dis_sample["lineP_x"]], [self.dis_sample["lineP_y"]], [self.dis_sample["lineP_z"]]])

        # macierz rotacji dla danych kątów
        if self.simplified_orientation:
            rot = self.get_rotation_matrix_simplified(yaw)
        else:
            rot = self.get_rotation_matrix(yaw, pitch, roll)

        # rzutowanie przemieszczeń lokalnych na globalne
        dis_sample_matrix_global = np.dot(rot, dis_sample_matrix_local)

        keys = ["lineP_x", "lineP_y", "lineP_z"]
        for i in range(3):
            self.dis_sample[keys[i]] = dis_sample_matrix_global[i][0]

    # położenie i orientacja we współrzędnych glabalnych
    def get_global_coordinates(self):
        # aktualne położenie = przemieszczenia we współrzędnych globalnych + poprzedniego położenia
        keys_pos = ["lineP_x", "lineP_y", "lineP_z"]
        for i in range(len(keys_pos)):
            self.pos_sample[keys_pos[i]] += self.dis_sample[keys_pos[i]]

        # pobranie orientacji prosto z ahrs, bez przeliczania z przyspieszeń
        keys = ["yaw", "pitch", "roll"]
        for key in keys:
            self.pos_sample[key] = self.dis_sample[key]

        self.pos_sample["time"] = self.acc_samples[0]["time"]

    def get_input_data(self):
        data = self.ahrs.get_inertial_navigation_data()
        self.compensate_constant_bias(data)
        self.cut_low_acc(data)
        return data

    # odejmuje od danych wejściowych stały błąd
    def compensate_constant_bias(self, data):
        keys = ["lineA_x", "lineA_y", "lineA_z"]
        for key in keys:
            data[key] -= self.constant_bias[key]

    # pomijanie pierwszych, niewłaściwych próbek
    def skip_samples(self):
        for i in range(self.SKIPPED_SAMPLES - 1):
            self.ahrs.get_inertial_navigation_data()
            time.sleep(self.SLEEP_TIME)

    def cut_low_acc(self, data):
        keys = ["lineA_x", "lineA_y", "lineA_z"]
        for key in keys:
            if -self.ACC_CUT_THRESHOLD < data[key] < self.ACC_CUT_THRESHOLD:
                data[key] = 0

    @staticmethod
    def get_rotation_matrix(yaw, pitch, roll):
        return np.array([[cos(pitch) * cos(yaw), cos(yaw) * sin(pitch) * sin(roll) - cos(roll) * sin(yaw),
                         sin(roll) * sin(yaw) + cos(roll) * cos(yaw) * sin(pitch)],
                        [cos(pitch) * sin(yaw), cos(roll) * cos(yaw) + sin(pitch) * sin(roll) * sin(yaw),
                         cos(roll) * sin(pitch) * sin(yaw) - cos(yaw) * sin(roll)],
                        [-sin(pitch), cos(pitch) * sin(roll), cos(pitch) * cos(roll)]])

    @staticmethod
    def get_rotation_matrix_simplified(yaw):
        return np.array([[cos(yaw), - sin(yaw), 0], [sin(yaw), cos(yaw), 0], [0, 0, 1]])

    def log_ahrs_data(self):
        while True:
            data = self.ahrs.get_inertial_navigation_data()
            print(data[time])
            msg = ""
            for key in data:
                msg += str(data[key]) + ", "
            msg += "\n"
            self.file_log_raw_data.write(msg)
            time.sleep(0.0025)

