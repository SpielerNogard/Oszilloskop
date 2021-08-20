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
        x_len=  200
        y_range=  [-10, 10]
        interval= 20
        self.Signal_gen = Signalgenerator
        self.x = []
        self.y = []
        self.length = 10
        self.triggered = False
        self.trigger_value = 2
        self.inverted = False
        for i in range (self.length):
            self.x.append(i)
            self.y.append(0)


        self.i = 0
        

        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        self.x = list(range(-10, x_len-10))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_ = self.figure.subplots()
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(self.x, y)
        self._ax_.grid()
        #self._ax_.axhline(y=0, color = "k")
        #self._ax_.axvline(x=0, color = "k")
        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y,), interval=interval, blit=False)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        
        y.append(round(self.give_me_new_poitn(), 2))  # Add new datapoint
        y = y[-self._x_len_:]  # Truncate list _y_
        #print(y)
        #self._line_.set_ydata(y)
        self._line_.set_data(self.x,y)
        return self._line_,

    def give_me_new_poitn(self):
        # Return your next y point
        
        self.i +=1
        #self.x.append(self.i) 
        #new_point = 3 * np.sin(2 * np.pi * self.i/60)
        #print(new_point)
        new_point = self.Signal_gen.new_point(self.i)
        #print(new_point)
        if self.inverted:
            new_point = -new_point

        if (self.inverted and new_point <-self.trigger_value) or (not self.inverted and new_point >self.trigger_value):
            self.triggered = True
        if not self.triggered:
            new_point = 0

            #self.y[self.t] = new_point

        #print(new_point)
        return(new_point)

    def set_time(self, time):
        print(time)

    def set_voltage(self, voltage):
        self._ax_.set_ylim(ymin= - voltage, ymax=voltage)
        self._y_range_ = voltage

    def set_trigger(self, trigger):
        print(trigger)

    def set_amplitude(self, amplitude):
        print(amplitude)
        self.Signal_gen.amplitude = int(amplitude)

    def set_frequenz(self, frequenz):
        print(frequenz)
        self.Signal_gen.frequency = int(frequenz)

    def set_inverted(self, invertet):
        self.inverted = invertet

    def set_generated_signal(self):
        pass

    def set_file_signal(self):
        pass

    def set_live_signal(self):
        pass

    def set_posx(self,value):
        pass

    def set_posy(self, value):
        pass
    
    
