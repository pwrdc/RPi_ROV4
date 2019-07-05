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
        if pinger_freq == 15000:
            phase_delta -= 0.0820
        print('Delta phase radian', phase_delta)
        angle_to_pinger = self.from_phase_to_angle(phase_delta, pinger_freq)
        angle_to_pinger = angle_to_pinger*180/numpy.pi
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
        wave_length = 1490/freq
        return numpy.arcsin((phase_delta*wave_length)/(2*numpy.pi*HYDROPHONES_DISTANCE))



    def getter2msg(self):
        return 0
    
if __name__ == '__main__':
    a = HydrophonesPair()
    a.get_angle(15000)
    
    