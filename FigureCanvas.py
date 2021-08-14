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


class MyFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''

    def __init__(self, x_len: int, y_range: List, interval: int) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        self.inverted = False


        self.i = 0
        n = np.linspace(0, 499, 500)
        self.d = 50 + 25 * (np.sin(n / 8.3)) + 10 * (np.sin(n / 7.5)) - 5 * (np.sin(n / 1.5))

        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        x = list(range(0, x_len))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_ = self.figure.subplots()
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y)

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y,), interval=interval, blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        y.append(round(self.get_next_datapoint(), 2))  # Add new datapoint
        y = y[-self._x_len_:]  # Truncate list _y_
        self._line_.set_ydata(y)

        return self._line_,

    def get_next_datapoint(self):
        self.i += 1
        if self.i > 499:
            self.i = 0
        new_datapoint = self.d[self.i]

        return self.d[self.i]

    def set_time(self, time):
        print(time)

    def set_voltage(self, voltage):
        self._ax_.set_ylim(ymin= - voltage, ymax=voltage)
        self._y_range_ = voltage

    def set_trigger(self, trigger):
        print(trigger)

    def set_amplitude(self, amplitude):
        print(amplitude)

    def set_frequenz(self, frequenz):
        print(frequenz)

    def set_inverted(self, invertet):
        self.inverted = invertet

    def set_generated_signal(self):
        pass

    def set_file_signal(self):
        pass

    def set_live_signal(self):
        pass

