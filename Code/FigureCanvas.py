from __future__ import annotations

import numpy
from matplotlib.backends.backend_qt5agg import FigureCanvas

import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import numpy as np

import time
import threading
import pyaudio

class MyFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''

    def __init__(self,Signalgenerator) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''

        self.abtastrate = 44100
        self.Signal_gen = Signalgenerator
        self.signal_generator_reader = SignalGeneratorReader(self.abtastrate, Signalgenerator)
        self.live_signal_reader = ValueReader(self.abtastrate)

        self.live_active = False
        self.generator_active = True

        self.trigger_x_offset_percent = 0
        self.trigger_position = 0
        self.point_to_update = 0

        self.number_of_boxes = 10
        self.time_per_box = 1
        self.voltage_per_box = 1

        self.offset_y_percent = 0
        self.offset_y = 0

        self.triggered = False
        self.trigger_percent = 0
        self.trigger_value = 0

        self.need_to_update = True

        self.smaller_than_trigger_found = False
        self.bigger_than_trigger_found = False
        self.inverted = False

        self.screen_filled = False
        self.interval = 33
        FigureCanvas.__init__(self, mpl_fig.Figure())

        # Store two lists _x_ and _y_
        self.x = np.linspace(0, 1, num=self.abtastrate)
        self.current_data_showing = [0] * self.abtastrate
        self.all_data = [0] * self.abtastrate
        self.combined_signals = []


        # Store a figure and ax
        self._ax_ = self.figure.subplots()
        self._line_, = self._ax_.plot(self.x, self.all_data)
        self._ax_.grid(which='major', axis='both')

        self.x_tick_boxes = np.linspace(0,self.time_per_box * (self.number_of_boxes), num=self.number_of_boxes+1)

        y_voltage_point = (self.voltage_per_box * self.number_of_boxes)/2

        self.y_tick_boxes = np.linspace(-y_voltage_point,y_voltage_point, num=self.number_of_boxes + 1)
        self._ax_.set_ylim(ymin=(-self.voltage_per_box + self.offset_y) * self.number_of_boxes / 2, ymax=(self.voltage_per_box + self.offset_y) * self.number_of_boxes / 2)

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(self.all_data,), interval=self.interval, blit=False)
        return

    def _update_canvas_(self, i, y) -> None:

        '''
        This function gets called regularly by the timer.

        '''
        signal_generator_values = self.signal_generator_reader.get_read_values()
        mic_values = self.live_signal_reader.get_read_values()
        shorter_array = mic_values

        "Die Länge der Arrays vom Signalgenerator und den Mikrophon Aufnahmen sind nicht immer gleich, daher werden Werte des Mikrophon gespeichert, während" \
        "beim Signalgenerator resampled wird, da dieses mit der Zeit die fehlende Anzahl der Werte einholen wird" \
        " Signalgenerator ~ 44110 Hz" \
        " Mikrophon ~ 44090 Hz "
        if len(signal_generator_values) > len(mic_values):
            self.signal_generator_reader.reset_values(0)
            self.live_signal_reader.reset_values(0)
            shorter_array = mic_values

        elif len(mic_values) > len(signal_generator_values):
            self.signal_generator_reader.reset_values(0)
            self.live_signal_reader.reset_values(len(mic_values) - len(signal_generator_values))
            shorter_array = signal_generator_values

        else:
            self.signal_generator_reader.reset_values(0)
            self.live_signal_reader.reset_values(0)

        self.combined_signals = []

        for i in range(len(shorter_array)):
            if self.generator_active and self.live_active:
                new_point = signal_generator_values[i] + self.offset_y + mic_values[i]
            elif self.live_active:
                new_point = self.offset_y + mic_values[i]
            else:
                new_point = signal_generator_values[i] + self.offset_y

            self.combined_signals.append(new_point)
            #self.all_data.append(new_point)
            #self.all_data.pop(0)
            self.look_for_trigger_condition(new_point)
            if self.triggered:
                self.update_point(new_point)
            else:
                pass
        self.update_all_data()

        if self.need_to_update:
            self._line_.set_ydata(self.current_data_showing)
            self.need_to_update = False
        return

    def reset_trigger(self):
        self.triggered = False
        self.smaller_than_trigger_found = False
        self.bigger_than_trigger_found = False

    def update_all_data(self):
        if len(self.combined_signals) >= len(self.all_data):
            self.all_data = self.combined_signals[len(self.combined_signals)-len(self.all_data):]
        else:
            self.all_data = numpy.append(self.all_data[len(self.combined_signals):], self.combined_signals)
    def update_point(self, new_point):
        if self.point_to_update >= len(self.all_data):
            self.point_to_update = self.trigger_position
            self.need_to_update = True
            self.reset_trigger()
            self.update_all_data()
            self.combined_signals = []
            self.current_data_showing = self.all_data[:]

        self.point_to_update += 1

    def look_for_trigger_condition(self, new_point):
        if not self.inverted and not self.smaller_than_trigger_found and new_point < self.trigger_value :
            self.smaller_than_trigger_found = True
        elif not self.inverted and self.smaller_than_trigger_found and new_point > self.trigger_value :
            self.bigger_than_trigger_found = True

        elif self.inverted and not self.bigger_than_trigger_found and new_point > self.trigger_value :
            self.bigger_than_trigger_found = True

        elif not self.inverted and self.bigger_than_trigger_found and new_point < self.trigger_value :
            self.smaller_than_trigger_found = True

        if self.smaller_than_trigger_found and self.bigger_than_trigger_found:
            self.triggered = True

    def set_time(self, time):
        self.time_per_box = time
        total_time = self.time_per_box * self.number_of_boxes

        number_of_values = int(total_time * self.abtastrate)
        self.x = np.linspace(0, total_time, num=number_of_values)
        self.all_data = [0] * number_of_values
        self.current_data_showing = [0] * number_of_values

        self.set_x_labels()
        self.point_to_update = self.trigger_position
        self._line_.set_data(self.x, self.current_data_showing)


    def set_x_labels(self):
        total_time = self.time_per_box * self.number_of_boxes
        trigger_position = self.trigger_x_offset_percent * total_time
        self.trigger_position = int(self.trigger_x_offset_percent * total_time * self.abtastrate)
        self.x_tick_boxes = np.linspace(0, total_time, num=self.number_of_boxes+1)

        "Trigger Position an letzter Stelle, sodass der Strich als letztes gezeichnet/beschriftet wird (wenn nicht, kann er von den leeren Labels überschrieben werden)"
        test_ticks = numpy.append(self.x_tick_boxes, trigger_position)
        self._ax_.set_xticks(test_ticks)

        "Entfernung der Beschriftung der Ticks, abgesehen von dem Trigger Tick, dieser wird mit Trigger beschrieben"
        labels = ["" for item in test_ticks]
        labels[-1] = "Trigger"
        self._ax_.get_xaxis().set_ticklabels(labels)
        self._ax_.set_xlim(xmin=0, xmax=total_time)

    def set_voltage(self, voltage):
        self.voltage_per_box = voltage
        self.set_y_labels()

        self.offset_y = self.offset_y_percent * self.voltage_per_box * 0.01 * self.number_of_boxes/2

    def set_y_labels(self):
        total_voltage = self.voltage_per_box * self.number_of_boxes
        self.trigger_value = self.trigger_percent * total_voltage / 2
        y_voltage_point = total_voltage / 2

        self.y_tick_boxes = np.linspace(-y_voltage_point, y_voltage_point, num=(self.number_of_boxes)+ 1)

        "Trigger Position an letzter Stelle, sodass der Strich als letztes gezeichnet/beschriftet wird (wenn nicht, kann er von den leeren Labels überschrieben werden)"
        test_ticks = numpy.append(self.y_tick_boxes, self.trigger_value)

        self._ax_.set_yticks(test_ticks)

        "Entfernung der Beschriftung der Ticks, abgesehen von dem Trigger Tick, dieser wird mit Trigger beschrieben"
        labels = ["" for item in test_ticks]
        labels[-1] = "Trigger"
        self._ax_.get_yaxis().set_ticklabels(labels)

        self._ax_.set_ylim(ymin=- y_voltage_point, ymax=y_voltage_point)

    def set_trigger(self, trigger):
        #self.trigger_percent = (trigger - 50) * 2

        self.trigger_percent = (trigger - 50) * 2 * 0.01
        #self.triggered = False
        #self.bigger_than_trigger_found = False
        #self.smaller_than_trigger_found = False

        self.set_y_labels()

    def set_amplitude(self, amplitude):
        self.Signal_gen.amplitude = int(amplitude)

    def set_frequenz(self, frequenz):
        self.Signal_gen.frequency = float(frequenz)

    def set_inverted(self, invertet):
        self.inverted = invertet

    def set_generated_signal(self):
        self.generator_active = True
        self.live_active = False

    def set_mikrofon(self):
        self.generator_active = False
        self.live_active = True

    def set_live_signal(self):
        pass

    def set_posx(self,value):
        self.trigger_x_offset_percent = (value+1) * 0.01
        self.set_x_labels()

    def set_posy(self, value):
        self.offset_y_percent = (value - 50) * 2
        self.offset_y = self.offset_y_percent * self.voltage_per_box * 0.01 * self.number_of_boxes/2

    
class ValueReader(threading.Thread):
    def __init__(self, abtastrate):
        super().__init__()
        self.read_values = []
        self.abtastrate = abtastrate
        self.start_time = time.perf_counter()

        "Als Daemon Thread stoppt dieser, falls das Hauptprogramm gestoppt wird (das Window geschlossen wurde), ich kümmere mich deshalb nicht zum sauberen schließen" \
        "dieses"
        self.setDaemon(True)
        self.p = pyaudio.PyAudio()
        self.chunk_size = int(self.abtastrate / 60)
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.abtastrate, input=True,
                        frames_per_buffer=self.chunk_size)

        self.total_amount_points = 0
        self.start()

    def soundplot(self):
        data = np.frombuffer(self.stream.read(self.chunk_size), dtype=np.float32)
        self.read_values.extend(data)
        self.total_amount_points += len(data)


    def run(self):
        while True:
            self.soundplot()


    def get_read_values(self):
        return self.read_values

    def reset_values(self, amount_left):
        self.read_values = self.read_values[len(self.read_values) - amount_left:]


class SignalGeneratorReader(threading.Thread):
    def __init__(self, abtastrate, Signalgenerator):
        super().__init__()
        self.signal_generator = Signalgenerator
        self.read_values = []
        self.abtastrate = abtastrate

        "i beschreibt den zurzeit zu messenden Punkt, während r beschreibt, wieviele Chunks bereits berechnet wurden"
        self.i = 0
        self.r = 0

        self.start_time = time.perf_counter()

        "Als Daemon Thread stoppt dieser, falls das Hauptprogramm gestoppt wird (das Window geschlossen wurde), ich kümmere mich deshalb nicht zum sauberen schließen" \
        "dieses"
        self.setDaemon(True)

        self.reads_per_second = 60
        self.chunk_size = int(self.abtastrate / self.reads_per_second)


        self.start()


    def read_chunk_of_values(self):
        #for j in range(self.chunk_size):
            #new_value = self.signal_generator.new_point(self.i * (1.0/self.abtastrate))
            #self.read_values.append(new_value)

        new_value = self.signal_generator.new_point(self.i/self.abtastrate, (self.i + self.chunk_size) / self.abtastrate, self.chunk_size)
        self.i += self.chunk_size
        self.r += 1
        self.read_values.extend(new_value)




    def run(self):
        while True:
            self.read_chunk_of_values()
            self.sleep()

    def sleep(self):

        "Berechnet, wie lange der Thread schlafen muss, sodass er die Messungen pro Sekunde einhält,"
        "konstante Schlafenszeit bezieht nicht die benötigte Zeit zur Bearbeitung mit ein, weswegen delta berechnet wird"

        delta = self.start_time + (self.r / self.reads_per_second) - time.perf_counter()
        if delta > 0:
            time.sleep(delta)

    def get_read_values(self):
        return self.read_values

    def reset_values(self, amount_left):
        self.read_values = self.read_values[len(self.read_values) - amount_left:]

    def resample_point(self, change_point):
        self.i += change_point

