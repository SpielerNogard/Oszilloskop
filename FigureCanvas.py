from __future__ import annotations
from typing import *
import sys
import os
from matplotlib.backends.qt_compat import QtCore, QtWidgets
# from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvas
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib as mpl
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import numpy as np
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QLCDNumber)

from scipy import signal
from Signalgenerator import SignalGenerator
import math
import time

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
        self.max_amount_values_saved = 100000
        self.x_offset = 1
        self.point_to_update = 0

        self.time = time.time()

        self.time_per_box = 1
        self.number_of_boxes = 10

        self.voltage_per_box = 1

        self.offset = 0
        self.interval= 16
        self.abtastrate = 44100
        self.show_y = []
        self.Signal_gen = Signalgenerator


        self.triggered = False
        self.trigger_value = 2
        self.inverted = False

        self.i = 0

        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._y_range_ = 10

        # Store two lists _x_ and _y_
        self.x = np.linspace(0,1, num=self.abtastrate)

        self.saved_y = [0] * self.abtastrate

        # Store a figure and ax
        self._ax_ = self.figure.subplots()
        self._line_, = self._ax_.plot(self.x, self.saved_y)
        self._ax_.grid(which='major', axis='both')

        self.x_tick_boxes = np.linspace(0,self.time_per_box * (self.number_of_boxes), num=self.number_of_boxes+1)

        y_voltage_point = (self._y_range_ * (self.number_of_boxes))/2
        self.y_tick_boxes = np.linspace(-y_voltage_point,y_voltage_point, num=self.number_of_boxes + 1)
        self._ax_.set_ylim(ymin=(-self._y_range_ + self.offset) * self.number_of_boxes / 2, ymax=(self._y_range_ + self.offset) * self.number_of_boxes / 2)

        self._ax_.set_xticks(self.x_tick_boxes)
        self._ax_.set_yticks(self.y_tick_boxes)



        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(self.saved_y,), interval=self.interval, blit=False)
        return

    def _update_canvas_(self, i, y) -> None:

        '''
        This function gets called regularly by the timer.

        '''
        #self.triggered = False
        old = self.time
        self.time = time.time()
        time_passed = self.time - old


        print(self.time - old)
        amount = round(self.abtastrate * time_passed)

        for i in range(amount):
            new_point = round(self.give_me_new_poitn(), 2)
            if (self.inverted and new_point <= -self.trigger_value) or (not self.inverted and new_point >= self.trigger_value):
                self.triggered = True
            if not self.triggered:
                continue

            if self.point_to_update >= len(self.saved_y):
                self.point_to_update = 0
                self.triggered = False

            self.saved_y[self.point_to_update] = new_point
            self.point_to_update += 1
            #self.saved_y.append(new_point)
            #self.saved_y.pop(0)



        #x_offset = round((len(self.saved_y) - len(self.x)) * self.x_offset)


        #self.show_y = self.saved_y[x_offset:x_offset + len(self.x)]

        self._line_.set_ydata(self.saved_y)
        return

    def give_me_new_poitn(self):
        # Return your next y point
        self.i += 1
        time_position = self.i * 1.0 / self.abtastrate

        new_point = self.Signal_gen.new_point(time_position)

        if self.inverted:
            new_point = -new_point

        return(new_point)

    def set_time(self, time):
        self.time_per_box = time
        total_time = self.time_per_box * self.number_of_boxes


        self.x_tick_boxes = np.linspace(0, total_time, num=self.number_of_boxes+1)

        self.x = np.linspace(0, 1 , num = math.ceil(self.abtastrate * total_time))
        self.saved_y = [0] * math.ceil(self.abtastrate * total_time)

        print(math.ceil(self.abtastrate * total_time))
        print(len(self.x))
        print(len(self.saved_y))

        self._ax_.set_xticks(self.x_tick_boxes)

        self._ax_.set_xlim(xmin=0, xmax=total_time)
        self._line_.set_data(self.x,self.saved_y)

        #self.x_offset = (time+1) * 0.01
        #self.saved_y = [0] * (time * 100)
        #self.x = list(range(-10, time * 100 -10))
        #self._ax_.set_xlim(xmin=-10, xmax=time*100)

    def set_voltage(self, voltage):
        self.voltage_per_box = voltage

        y_voltage_point = (self.voltage_per_box * (self.number_of_boxes)) / 2
        self.y_tick_boxes = np.linspace(-y_voltage_point * 2, y_voltage_point * 2, num=(self.number_of_boxes) * 2 + 1)

        self._ax_.set_yticks(self.y_tick_boxes)

        self._y_range_ = voltage
        self._ax_.set_ylim(ymin=(-self._y_range_ + self.offset) * self.number_of_boxes / 2, ymax=(self._y_range_ + self.offset) * self.number_of_boxes / 2)


    def set_trigger(self, trigger):
        self.trigger_value = trigger

    def set_amplitude(self, amplitude):
        print(amplitude)
        self.Signal_gen.amplitude = int(amplitude)

    def set_frequenz(self, frequenz):
        print(frequenz)
        self.Signal_gen.frequency = float(frequenz)

    def set_inverted(self, invertet):
        self.inverted = invertet

    def set_generated_signal(self):
        pass

    def set_file_signal(self):
        pass

    def set_live_signal(self):
        pass

    def set_posx(self,value):
        self.x_offset = (value+1) * 0.01


    def set_posy(self, value):
        self.offset = (value - 50) * 2
        self.offset = self.offset * self._y_range_ * 0.01

        self._ax_.set_ylim(ymin=(-self._y_range_ + self.offset) * self.number_of_boxes / 2, ymax=(self._y_range_ + self.offset) * self.number_of_boxes / 2)
    
    
