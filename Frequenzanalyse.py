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
from scipy.fft import fft, fftfreq

class Frequenzcanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''

    def __init__(self,myFig) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''

        self.myFig = myFig
        x_len =  2000
        y_range=  [0, 100]
        interval= 2
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
        n = np.linspace(0, 499, 500)
        self.d = 50 + 25 * (np.sin(n / 8.3)) + 10 * (np.sin(n / 7.5)) - 5 * (np.sin(n / 1.5))

        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        self.x = list(range(0, x_len))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_ = self.figure.subplots()
        self._ax_.set_ylim(ymin=0, ymax=5)
        self._line_, = self._ax_.plot(self.x, y)

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y,), interval=interval, blit=False)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        print(self.myFig.saved_y[-1])
        y.append(round(self.give_me_new_poitn(), 2))  # Add new datapoint
        y = y[-self._x_len_:]  # Truncate list _y_

        # Number of sample points

        N = len(self.x)

        # sample spacing

        T = self._interval / 1000

        yf = fft(y)[0:N // 2]

        xf = fftfreq(N, T)[:N // 2]
        #print (y)
        self._ax_.set_xlim(xmin=xf[0], xmax=xf[-1])

        #self._ax_.set_xlim(xmin=30, xmax=70)
        #self._line_.set_ydata(y)
        self._line_.set_data(xf, 2.0 / N * np.abs(yf))
        return self._line_,

    def give_me_new_poitn(self):
        # Return your next y point
        self.i +=1
        new_point = 3 * np.sin(2 * np.pi * 70 * self.i * self._interval / 1000)
        if self.inverted:
            new_point = -new_point

        if (self.inverted and new_point <-self.trigger_value) or (not self.inverted and new_point >self.trigger_value):
            self.triggered = True
        if not self.triggered:
            new_point = 0

            #self.y[self.t] = new_point

        return(new_point)

    

