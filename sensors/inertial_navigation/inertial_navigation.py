"""
TODO:
integracja (oczywiście)
czy w get_global_displacement kąty nie będą przyjmowały niewłaściwych wartości
    przy przejściu przez -pi/2 i pi/2 między próbkami (patrz yaw_wykres.png)
initial_state, razem z początkową orientacją (tylko yaw)
    (orientacja z AHRS -> orientacja względem lokalnego układu, np. zwiazanego z basenem)
orientacja AHRS -> orientacja łodzi (bo może być krzywo zamontowany)
test na gotowych danych z ahrs.csv
"""

from sensors.ahrs import ahrs
import numpy as np
from math import sin, cos

class InertialNavigation():
    def __init__(self, ahrs, initial_state, is_orientation_simplified=False):
        self.ahrs = ahrs
        self.is_orientation_simplified = is_orientation_simplified

        # słownik wejściowy z ahrs z wartościami 0
        acc_sample_template = self.ahrs.get_all_data()
        for key in acc_sample_template:
            acc_sample_template[key] = 0

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
        self.pos_sample = initial_state.copy()

    # powinno być wywoływane cyklicznie, dla każdej próbki z AHRS
    def run(self):
        # przesunięcie próbek, dodanie nowej próbki z AHRS
        self.acc_samples[2] = self.acc_samples[1]
        self.acc_samples[1] = self.acc_samples[0]
        self.acc_samples[0] = self.ahrs.get_all_data()
        self.vel_samples[1] = self.vel_samples[0]

        # pobranie orientacji prosto z ahrs, bez przeliczania z przyspieszeń
        keys = ["yaw", "pitch", "roll"]
        for key in keys:
            self.dis_sample[key] = self.acc_samples[0]["key"]
            self.pos_sample[key] = self.acc_samples[0]["key"]

        # przemieszczenie w lokalnym układzie współrzędnych
        self.get_internal_displacement()

        # przeniesienie lokalnych przemieszczeń na układ globalny
        self.get_global_displacement()

        # dodanie przemieszczeń do poprzedniej pozycji
        self.get_global_coordinates()

    # przemieszczenie we współrzędnych wewnętrznych
    def get_internal_displacement(self):
        self.vel_samples[0]["time"] = self.acc_samples[0]["time"]
        # obliczenia dla wszystkich kierunków
        keys_acc = ["lineA_x", "lineA_y", "lineA_z"]
        keys_vel = ["lineV_x", "lineV_y", "lineV_z"]
        keys_pos = ["lineP_x", "lineP_y", "lineP_z"]
        for i in range(len(keys_acc)):
            # żeby nie było dzielenia przez 0
            if self.acc_samples[1]["time"] == 0:
                self.vel_samples[0][keys_vel[i]] = 0
            else:
                # całkowanie numeryczne metodą trapezów
                self.vel_samples[0][keys_vel[i]] += 0.5 * (
                            self.acc_samples[0][keys_acc[i]] + self.acc_samples[1][keys_acc[i]]) * (
                                                            self.acc_samples[0]["time"] - self.acc_samples[1]["time"])
            self.dis_sample[keys_pos[i]] = 0.5 * (
                        self.vel_samples[0][keys_vel[i]] + self.vel_samples[1][keys_vel[i]]) * (
                                                   self.vel_samples[0]["time"] - self.vel_samples[1]["time"])

    # przemieszczenie we współrzędnych globalnych
    def get_global_displacement(self):
        # obroty o kąt początkowy + połowa zmiany kąta ( = średnia kątów z dwóch kolejnych próbek)
        # to nie jest żadne przybliżenie tylko dokładna wartość. i mogę to udowodnić!
        yaw = (self.pos_sample["yaw"] + self.dis_sample["yaw"]) / 2
        pitch = (self.pos_sample["pitch"] + self.dis_sample["pitch"]) / 2
        roll = (self.pos_sample["roll"] + self.dis_sample["roll"]) / 2
        dis_sample_matrix_local = np.array(
            [[self.dis_sample["lineP_x"]], [self.dis_sample["lineP_y"]], [self.dis_sample["lineP_z"]]])

        # macierz rotacji dla danych kątów
        if(self.is_orientation_simplified):
            rot = self.get_rotation_matrix_simplified(yaw)
        else:
            rot = self.get_rotation_matrix(yaw, pitch, roll)

        # rzutowanie przemieszczeń lokalnych na globalne
        dis_sample_matrix_global = np.dot(rot, dis_sample_matrix_local)

        keys = ["lineP_x", "lineP_y", "lineP_z"]
        for i in range(3):
            self.dis_sample[keys[i]] = dis_sample_matrix_global[i]

    # aktualne położenie = przemieszczenia we współrzędnych globalnych + poprzedniego położenia
    def get_global_coordinates(self):
        keys_pos = ["lineP_x", "lineP_y", "lineP_z"]
        for i in range(len(keys_pos)):
            self.pos_sample[keys_pos[i]] += self.dis_sample[keys_pos[i]]

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


