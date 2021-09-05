import numpy as np
import matplotlib.pylab as plt
import scipy.signal as sgnl
import sched, time


from matplotlib.animation import FuncAnimation

from PyQt5.QtCore import QTimer

from scipy.io.wavfile import read


class oszilloskop:
    samplerate = 44100
    time_field = 1
    amplitude_field = 1
    trigger = 0
    all_current_values = None
    type = "roundabout"
    current_point_field = 0

class the_plot:
    def __init__(self, length):
        self.x = []
        self.y = []
        self.length = length
        self.triggered = False
        self.trigger_value = 2
        self.inverted = True

        for i in range (length):
            self.x.append(i)
            self.y.append(0)

        self.t = 0
        self.time = 0
        self.osz = oszilloskop()
        self.plot = plt
        self.plot.plot(self.x,self.y)
        self.plot.xlim(0,100)
        self.plot.ylim(-3,3)

        self.animation = None

    def add_information_to_graph(self, y):
        pass

    def start_animation(self):
        def update(i):
            new_point = 3 * np.sin(2 * np.pi * self.time/60)

            if self.inverted:
                new_point = -new_point

            if (self.inverted and new_point <-self.trigger_value) or (not self.inverted and new_point >self.trigger_value):
                self.triggered = True
            if not self.triggered:
                new_point = 0

            #self.y[self.t] = new_point

            self.y.pop(0)
            self.y.append(new_point)

            self.t += 1
            if self.t >= len(self.x):
                self.t = 0




            self.plot.cla()
            self.plot.xlim(0, self.length)
            self.plot.ylim(-3, 3)
            self.plot.plot(self.x,self.y)
            self.time += 1
        self.animation = FuncAnimation(self.plot.gcf(), update, interval=100)

    def show_plot(self):
        self.plot.show()

def Main():

    s = sched.scheduler(time.time, time.sleep)

    def do_something(sc):
        print("Doing stuff...")
        # do your stuff
        s.enter(0.60, 1, do_something, (sc,))


    test_plot = the_plot(100)

    test_plot.start_animation()

    test_plot.show_plot()


    #s.enter(0.60, 1, do_something, (s,))
    #s.run()

    print("HEY")







if __name__ == "__main__":
    Main()