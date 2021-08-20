import numpy as np
from scipy import signal

class SignalGenerator(object):
    def __init__(self):
        self.start = 0
        self.stop = 100
        self.sample_rate = 480000
        self.frequency =50
        self.amplitude = 3

        self.signal_to_generate = "Sinus"
        self.time_vector = None
        self.Signal = None
        #self.generate_time_vector()
        #self.generate_sinus(0)
        
        self.new_point(0)
    def new_point(self,i):
        self.i = i
        
        if self.signal_to_generate == "Sinus":
            self.generate_sinus()
        elif self.signal_to_generate == "Square":
            self.generate_square()
        elif self.signal_to_generate == "Sawtooth":
            self.generate_sawtooth()
        return(self.Signal)

    def generate_time_vector(self):
        self.time_vector = np.linspace(start=self.start,stop=self.stop,num=self.sample_rate)

    def generate_sinus(self):
        #Sinus = self.amplitude*np.sin(2*np.pi*self.frequency*self.time_vector)
        Sinus = self.amplitude*np.sin(2*np.pi* self.i/self.frequency)
        self.Signal = Sinus
        return(Sinus)

    def generate_square(self):
        #Square = signal.square(2*np.pi*self.frequency*self.time_vector)
        Square = self.amplitude*signal.square(2*np.pi* self.i/self.frequency)
        
        self.Signal = Square
        return(Square)

    def generate_sawtooth(self):
        #t = np.linspace(start=start,stop=stop,num=sample_rate,endpoint=True)
        #Sawtooth = signal.sawtooth(2*np.pi*Frequency*t)
        Sawtooth = self.amplitude*signal.sawtooth(2*np.pi* self.i/self.frequency)
        self.Signal = Sawtooth
        return(Sawtooth)

    def generate_chirp(self,start,stop,sample_rate,Frequency):
        t = np.linspace(start=start,stop=stop,num=sample_rate,endpoint=True)
        Chirp = signal.chirp()

    def generate_gauspulse(self,start,stop,sample_rate,Frequency,place):
        t = np.linspace(start=start,stop=stop,num=sample_rate,endpoint=True)
        real, imaginary, envelope = signal.gausspulse(t, fc = Frequency, retquad = True, retenv = True)

    def generate_unitimpulse(self,start,stop,sample_rate,place):
        t = np.linspace(start=start,stop=stop,num=sample_rate,endpoint=True)
        lenght_impulse = len(t)
        impulse = signal.unit_impulse(lenght_impulse,place)
        return(impulse)