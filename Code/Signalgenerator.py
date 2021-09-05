import numpy as np
from scipy import signal

class SignalGenerator(object):
    def __init__(self):
        self.sample_rate = 500
        self.frequency = 20
        self.amplitude = 0.1

        self.start = 0
        self.end = 0
        self.amount = 0

        self.signal_to_generate = "Sinus"
        self.time_vector = None
        self.Signal = None

    def new_point(self,start, end, amount):
        self.start = start
        self.end = end
        self.amount = amount

        self.generate_time_vector(start, end, amount)
        
        if self.signal_to_generate == "Sinus":
            self.generate_sinus()
        elif self.signal_to_generate == "Square":
            self.generate_square()
        elif self.signal_to_generate == "Sawtooth":
            self.generate_sawtooth()
        return(self.Signal)

    def generate_time_vector(self, start, end, amount):
        self.time_vector = np.linspace(start=start,stop=end ,num=amount)

    def generate_sinus(self):
        Sinus = self.amplitude*np.sin(2*np.pi* self.frequency * self.time_vector)
        self.Signal = Sinus
        return(Sinus)

    def generate_square(self):
        Square = self.amplitude*signal.square(2*np.pi* self.frequency * self.time_vector)
        self.Signal = Square
        return(Square)

    def generate_sawtooth(self):
        Sawtooth = self.amplitude*signal.sawtooth(2*np.pi* self.frequency * self.time_vector)
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