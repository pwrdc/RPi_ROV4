from hydrophones_itf import IHydrophonesPair
import numpy
import soundfile as sf
import os

HYDROPHONES_DISTANCE = 0.018
#IN METERS!

class HydrophonesPair(IHydrophonesPair):
    '''
    Class to handle hydrophones signal and
    calculate angle
    '''
    def __init__(self):
        self.wav_file_count = 0

    #@Base.multithread_method
    def get_angle(self, pinger_freq):
        os.system('arecord -c 2 -D plughw:0,0 -f S16_LE -r96000 --duration=2 signal%s.wav' %(str(self.wav_file_count)))
        data, fs = sf.read('signal%s.wav' %(str(self.wav_file_count)))
        self.wav_file_count += 1
        data = data.transpose()
        self.left_fft = numpy.fft.fft(data[0])
        right_fft = numpy.fft.fft(data[1])
        print('Signal len',len(right_fft))
        interesting_freq = len(data[0])*pinger_freq/96000
        max_value_at = self.find_max(int(interesting_freq))
        print('Max value at ',max_value_at/2,'Hz')
        phase_delta = numpy.angle(right_fft[max_value_at], deg = False) - numpy.angle(self.left_fft[max_value_at],deg = False)
        if phase_delta > numpy.pi:
            phase_delta = phase_delta-2*numpy.pi
        elif phase_delta < -numpy.pi:
            phase_delta = 2*numpy.pi + phase_delta
        if pinger_freq == 15000:
            phase_delta -= 0.0820
        print('Delta phase radian', phase_delta)
        angle_to_pinger = self.from_phase_to_angle(phase_delta, pinger_freq)
        print('Angle to pinger in degrees',angle_to_pinger)


        '''
        TESTS
        '''
        plik = open('test_hydrofonow.txt','a+')
        plik.write('\nBadana czestotliwosc ')
        plik.write(str(max_value_at/2))
        plik.write('\nRoznica faz w radianach ')
        plik.write(str(phase_delta))
        plik.write('\nKat do hydrofonow w stopniach ')
        plik.write(str(angle_to_pinger))
        plik.write('\n')
        plik.close()
        #END OF TEST

        return angle_to_pinger
        

    def find_max(self,region_center):
        max_value_at = 0
        max_value = 0
        for i in range(region_center-5000,region_center+5000):
            if numpy.absolute(self.left_fft[i])>max_value:
                max_value = numpy.absolute(self.left_fft[i])
                max_value_at = i
        return max_value_at
    
    def from_phase_to_angle(self, phase_delta, freq):
        if freq == 15000:
            angle = 11.068*phase_delta**3 + 3.8552*phase_delta**2 -101.34*phase_delta + 16.389
        elif freq == 20000:
            angle = -9.7242*phase_delta**3 - 0.5636*phase_delta**2 -49.982*phase_delta+19.794
        elif freq == 25000:
            angle = 3.7762*phase_delta**3 - 1.1658*phase_delta**2 - 64.274*phase_delta + 7.124
        elif freq == 30000:
            angle = -0.5659*phase_delta**3 - 4.0424*phase_delta**2 - 48.973*phase_delta +3.2175
        elif freq == 40000:
            angle = -5.4937*phase_delta**3 + 3.1092*phase_delta**2 - 17.501*phase_delta - 3.0393
        else:
            angle = None
        if angle < -90:
            angle = -90
        elif angle > 90:
            angle = 90
        return angle



    def getter2msg(self):
        return 0
    
if __name__ == '__main__':
    a = HydrophonesPair()
    a.get_angle(40000)
    a.get_angle(40000)
    a.get_angle(40000)
    a.get_angle(40000)
    a.get_angle(40000)
    
    