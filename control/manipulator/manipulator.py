import numpy as np
from math import sin, cos, pi, sqrt, atan, acos, fabs


# na końcu przykłady użycia funkcji
class Manipulator:

# tworząc obiekt klasy Manipulator deklarujesz listę długości kolejnych członów, listę ograniczeń kątów w przegubach
# (min i max), ograniczenia prędkości i przyspieszeń kątowych (lista) i liniowych (zwykłe int)
# kolejność od podstawy
    def __init__(self, L, o_lim, v_kat_max, a_kat_max, v_max, a_max):
        self.L = L
        self.o_lim = o_lim
        self.v_kat_max = v_kat_max
        self.a_kat_max = a_kat_max
        self.v_max = v_max
        self.a_max = a_max
        self.compute_const()

# obliczenie stałych przy pierwszym uruchomieniu - OPTYMALIZACJA!!! xD
    def compute_const(self):
        self.range_max = sqrt(self.L[0]**2+self.L[1]**2) + sqrt(self.L[2]**2 + (self.L[3]+self.L[4]+self.L[5])**2)
        self.range_min_sqr = self.L[0]**2 + self.L[1]**2 + self.L[2]**2 + (self.L[3]+self.L[4]+self.L[5])**2 \
                             - 2*sqrt(self.L[0]**2+self.L[1]**2)*sqrt(self.L[2]**2
                             +(self.L[3]+self.L[4]+self.L[5])**2)*cos(pi+atan(self.L[0]/self.L[1])
                             - atan((self.L[3]+self.L[4]+self.L[5])/self.L[2])+self.o_lim[2])

        self.o1_numerator = self.L[0]**2 + self.L[1]**2 - self.L[2]**2 - (self.L[3]+self.L[4]+self.L[5])**2
        self.o1_denominator = 2*sqrt(self.L[0]**2+self.L[1]**2)
        self.o1_add = - atan(self.L[1]/self.L[0])

        self.o2_numerator = self.L[0]**2+self.L[1]**2+self.L[2]**2+(self.L[3]+self.L[4]+self.L[5])**2
        self.o2_denominator = 2*sqrt(self.L[0]**2+self.L[1]**2)*sqrt(self.L[2]**2+(self.L[3]+self.L[4]+self.L[5])**2)
        self.o2_add = - pi - atan(self.L[0]/self.L[1]) + atan((self.L[3]+self.L[4]+self.L[5])/self.L[2])

# używać do obliczania współrzędnej początkowej do interpolacji liniowej
# możliwe, że w ogóle się nie przyda, no ale to podstawa
# o_input - list, tuple, numpy.array, co tam chcecie
# zwraca współrzędne punktu w formacie numpy.array
    def forward_kinematics(self, o_input):
        o = np.asarray(o_input)
        return np.array([self.L[0]*cos(o[0]) - self.L[1]*sin(o[0]) - self.L[2]*sin(o[0]+o[1])
                        + (self.L[3]+self.L[4]+self.L[5])*cos(o[0]+o[1]),
                        self.L[0]*sin(o[0]) + self.L[1]*cos(o[0]) + self.L[2]*cos(o[0]+o[1])
                        + (self.L[3]+self.L[4]+self.L[5])*sin(o[0]+o[1]),
                        o[2]])

# używane przez linear_interpolation, nie wywoływać samodzielnie
# zwraca list (!) współrzędnych wewnętrznych i czasów, w których mają zostać osiągnięte w formacie [o[0], o[1], o[2], t]
# w przypadku braku możliwości osiągnięcia któregoś z punktów zwraca pustą list
    def inverse_kinematics(self, p):
        o = np.empty_like(p)
        for i in range(p.shape[0]):
            if p[i, 0] > 0 and sqrt(p[i, 0]**2 + p[i, 1]**2) < self.range_max and \
                    p[i, 0]**2+p[i, 1]**2 >= self.range_min_sqr:
                o[i, 0] = acos((self.o1_numerator + p[i, 0]**2 + p[i, 1]**2)
                               / (self.o1_denominator*sqrt(p[i, 0]**2 + p[i, 1]**2))) \
                               + self.o1_add + atan(p[i, 1]/p[i, 0])
                o[i, 1] = acos((self.o2_numerator - p[i, 0]**2 - p[i, 1]**2)/self.o2_denominator) + self.o2_add
                o[i, 2] = p[i, 2]
                o[i, 3] = p[i, 3]
                if o[i, 0] < self.o_lim[o] or o[i, 0] > self.o_lim[1] or o[i, 1] < self.o_lim[2] or \
                        o[i, 1] > self.o_lim[3] or o[i, 2] < self.o_lim[4] or o[i, 2] > self.o_lim[5]:
                    return []
            else:
                return []
        return o.tolist()

# ruch z punktu o_s_input do o_k_input bez określania trajektorii (podaj współrzędne wewnętrzne)
# res - rozdzielczość interpolacji int >= 1
# o_k_input, o_s_input - list, tuple, numpy.array, co tam chcecie
# zwraca list (!) współrzędnych wewnętrznych i czasów, w których mają zostać osiągnięte w formacie [o[0], o[1], o[2], t]
    def pivot_interpolation(self, o_k_input, o_s_input, res):
        o_k = np.asarray(o_k_input)
        o_s = np.asarray(o_s_input)
        T_all = []
        for i in range(3):
            T_all.append([])
            T_all[i].append(sqrt((6*fabs(o_k[i]-o_s[i]))/self.a_kat_max[i]))
            T_all[i].append((3*fabs(o_k[i]-o_s[i]))/(2*self.v_kat_max[i]))
        T = max(max(T_all))
        inc = T/res
        o = np.empty([res+1, 4])
        for i in range(0, res+1):
            t = i*inc
            o[i, :] = np.concatenate((o_s + (3*t**2/T**2 - 2*t**3/T**3)*(o_k - o_s), [t]))
        return o.tolist()

# ruch z punktu p_s_input do p_k_input po linii prostej, punkty muszą mieć taką samą orientację
# res - rozdzielczość interpolacji int >= 1
# p_k_input, p_s_input - list, tuple, numpy.array, co tam chcecie
# wywołuje kinematyka_odwrotna
# w przypadku podania nieprawidłowych punktów zwraca pustą list

    def linear_interpolation(self, p_k_input, p_s_input, res):
        p_k = np.asarray(p_k_input)
        p_s = np.asarray(p_s_input)
        if p_k[2] == p_s[2]:
            T = max([sqrt((6 * sqrt((p_k[0] - p_s[0]) ** 2 + (p_k[1] - p_s[1]) ** 2)) / self.a_max),
                     (3 * sqrt((p_k[0] - p_s[0]) ** 2 + (p_k[1] - p_s[1]) ** 2)) / (2 * self.v_max)])
            inc = T/res
            p = np.empty([res+1, 4])
            for i in range(0, res+1):
                t = i*inc
                p[i, :] = np.concatenate((p_s + (3*t**2/T**2 - 2*t**3/T**3)*(p_k - p_s), [t]))
            return self.inverse_kinematics(p)
        else:
            return []


#manipulator = Manipulator([10, 300, 10, 330, 81, 67], [-0.001, pi/4, -pi/4, pi/4, -pi, pi], [10, 10, 10], [2, 2, 2], 1000, 1000)

# do sterowania używaj tylko funkcji interpolacyjnych
#o = manipulator.pivot_interpolation([0, 0, 0], [pi/2, pi/4, pi/8], 50)
#o = manipulator.linear_interpolation([450, 310, 0], [400, 310, 0], 5)
