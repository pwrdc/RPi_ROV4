from sensors.hydrophones.hydrophones_itf import IHydrophonesPair
from sensors.base_sensor import BaseSensor
import numpy
from scipy.io import wavfile
import os

HYDROPHONES_DISTANCE = 0.018
#IN METERS!

class HydrophonesPair(BaseSensor,IHydrophonesPair):
    '''
    Class to handle hydrophones signal and
    calculate angle
    '''
    def __init__(self):
        self.wav_file_count = 0

    #@Base.multithread_method
    def get_angle(self, pinger_freq):
        os.system('arecord -c 2 -D plughw:0,0 -f S16_LE -r96000 --duration=2 signal%s.wav' %(str(self.wav_file_count)))
        fs, data = wavfile.read('signal%s.wav' %(str(self.wav_file_count)))
        self.wav_file_count += 1
        data = data.transpose()
        self.left_fft = numpy.fft.fft(data[0])
        right_fft = numpy.fft.fft(data[1])
        interesting_freq = len(data[0])*pinger_freq/96000
        max_value_at = self.find_max(interesting_freq)
        phase_delta = numpy.angle(right_fft[max_value_at], deg = True) - numpy.angle(self.left_fft[max_value_at],deg = True)
        if pinger_freq == 15000:
            phase_delta += 4.7
        angle_to_pinger = self.from_phase_to_angle(phase_delta, pinger_freq)
        angle_to_pinger = angle_to_pinger*180/numpy.pi
        '''
        TESTS
        '''
        plik = open('test_hydrofonow.txt','w')
        plik.write('\nRoznica faz w stopniach ')
        plik.write(str(phase_delta))
        plik.write('\nKat do hydrofonow w stopniach ')
        plik.write(str(angle_to_pinger))
        #END OF TEST

        return angle_to_pinger
        

    def find_max(self,region_center):
        max_value_at = 0
        max_value = 0
        for i in range(region_center-2500,region_center+2500):
            if numpy.absolute(self.left_fft[i])>max_value:
                max_value = numpy.absolute(self.left_fft[i])
                max_value_at = i
        return i
    
    def from_phase_to_angle(self, phase_delta, freq):
        wave_length = 1490/freq
        phase_delta_radian = phase_delta*numpy.pi/180
        return numpy.arcsin((phase_delta_radian*wave_length)/(2*numpy.pi*HYDROPHONES_DISTANCE))



    def getter2msg(self):
        return 0