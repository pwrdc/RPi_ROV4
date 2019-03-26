import pigpio

import time





class EngineDriver():

	

	engines_ready = False

	frequency = 500

	startup_time = 5

	stop = 192

	

	old_min = -1

	old_max = 1

	new_max = 255

	new_min = 128

	engines_dict = {"fl" : 12}#, "fr" : 3, "bl" : 4, "br" : 5,"vl" : 6,"vr" : 7,"vb" : 8}

	set_dict = {"fl" : False}#, "fr" : False, "bl" : False, "br" : False,"vl" : False,"vr" : False,"vb" : False}

	old_dict = {"fl" : 192}#, "fr" : 192, "bl" : 192, "br" : 192,"vl" : 192,"vr" : 192,"vb" : 192}

	def __init__(self):

		self.pi = pigpio.pi()

		print("Ustawianie silników")

		for val in self.engines_dict.values():

			self.pi.set_PWM_dutycycle(val,self.stop)

			self.pi.set_PWM_frequency(val,self.frequency)

		time.sleep(5)

		self.engines_ready = True

		print("Silniki gotowe")

		#aby sterownik się zainicjował poprawnie, trzeba kila sekund dawać sygnał o wypełnieniu 75%

		# i okresie 2000us

	

	def __del__(self):

		for val in self.dictionary.values():

			self.pi.set_PWM_dutycycle(val,stop)

		self.pi.stop()

	

	def set_engines(self,dictionary):

		for key, val in dictionary.items():

			dictionary[key] = (((val - self.old_min) * (self.new_max - self.new_min)) / (self.old_max - self.old_min)) + self.new_min

		while True:

			for key, val in dictionary.items():

				if int(dictionary[key]) == int(self.old_dict[key]):

					self.set_dict[key] = True

				elif dictionary[str(key)] < self.old_dict[str(key)]:

					self.old_dict[key] = self.old_dict[key]-1

				elif dictionary[str(key)] > self.old_dict[str(key)]:

					self.old_dict[key] = self.old_dict[key]+1

				self.pi.set_PWM_dutycycle(self.engines_dict[key],self.old_dict[key])

				print(self.old_dict[key], dictionary[key])

				if all(is_set is True for is_set in self.set_dict.values()):

                                    print("break")

                                    for key in self.set_dict.keys():

                                        self.set_dict[key] = False

                                    return





def compute_motor_powers_limited(front, right, up, yaw):

    """

    front, right, up, yaw [-1,1]

    fl (front left), fr, bl, br, vl, vr, vb [-1,1]

    przelicza prędkości na moc silników.

    fl przyjmuję początkowo jako 1,

    potem optymalizuję wartości za pomocą correction.

    optymalizacja - równe, najmniejsze możliwe obciążenie silników



    Wersja ograniczona - parametry z zakresu [-1,1] w dowolnej konfiguracji

    pełna moc możliwa jedynie przy ruchu na ukos (front = +-1 right = +-1)

    """



    vlvr_to_vb = 0.5

    # stosunek mocy silników pionowych przednich do tylnego

    # do konfiguracji

    # zakres (0,1)



    fl = 1

    fr = fl - right - yaw

    bl = fl - front - yaw

    br = fl - right - front

    vb = up

    vl = up * vlvr_to_vb



    correction = -0.5 * (min(fl, fr, bl, br) + max(fl, fr, bl, br))



    fl += correction

    fr += correction

    bl += correction

    br += correction



    motor_powers = {

        "fl": fl,

        "fr": fr,

        "bl": bl,

        "br": br,

        "vl": vl,

        "vr": vl,

        "vb": vb

    }

    return motor_powers





def compute_motor_powers_unlimited(front, right, up, yaw):

    """

    front, right, up, yaw [-1,1]

    fl (front left), fr, bl, br, vl, vr, vb [-1,1]

    przelicza prędkości na moc silników.

    fl przyjmuję początkowo jako 1,

    potem optymalizuję wartości za pomocą correction.

    optymalizacja - równe, najmniejsze możliwe obciążenie silników



    Wersja bez ograniczenia mocy - parametry z zakresu [-1,1] takie, że:

    abs(front) + abs(right) <= 1

    abs(front) + abs(yaw) <= 1

    abs(right) + abs(yaw) <= 1

    Pełna moc możliwa w każdym kierunku

    należy nałożyć dodatkowe ograniczenia przy wyznaczaniu parametrów!

    """



    vlvr_to_vb = 0.5    # stosunek mocy silników pionowych przednich do tylnego. do konfiguracji



    fl = 1

    fr = fl - 2*right - 2*yaw

    bl = fl - 2*front - 2*yaw

    br = fl - 2*right - 2*front

    vb = up

    vl = up * vlvr_to_vb



    correction = -0.5 * (min(fl, fr, bl, br) + max(fl, fr, bl, br))



    fl += correction

    fr += correction

    bl += correction

    br += correction



    motor_powers = {

        "fl": fl,

        "fr": fr,

        "bl": bl,

        "br": br,

        "vl": vl,

        "vr": vl,

        "vb": vb

    }

    return motor_powers





print(compute_motor_powers_limited(1, 0, 0, 0))

print(compute_motor_powers_unlimited(1, 0, 0, 0))



"""

funkcje różnią się tylko współczynnikami przy parametrach,

równie dobrze w pierwszej funkcji można by podawać parametry w zakresie [-2,2]

i by wyszło na to samo.

compute_motor_powers_limited(2, 0, 0, 0) = compute_motor_powers_unlimited(1, 0, 0, 0)

compute_motor_powers_limited(1, 0, 0, 0) = compute_motor_powers_unlimited(0.5, 0, 0, 0)

dla mnie lepsza ta druga funkcja

"""
