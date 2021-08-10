#####################################################################################
#                                                                                   #
#                PLOT A LIVE GRAPH IN A PYQT WINDOW                                 #
#                EXAMPLE 2                                                          #
#               ------------------------------------                                #
# This code is inspired on:                                                         #
# https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/speeding-up-the-plot-animation  #
#                                                                                   #
#####################################################################################

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
        QVBoxLayout, QWidget,QLCDNumber)

class ApplicationWindow(QtWidgets.QMainWindow):
    '''
    The PyQt5 main window.

    '''
    def __init__(self):
        super().__init__()
        # 1. Window settings
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("Oszilloskop")
        self.frm = QtWidgets.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: #eeeeec; }")
        self.lyt = QGridLayout()
        self.frm.setLayout(self.lyt)
        self.setCentralWidget(self.frm)
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftGroupBox()
        self.createBottomRightGroupBox()
        self.lyt.addWidget(self.topLeftGroupBox, 1, 0)
        self.lyt.addWidget(self.topRightGroupBox, 1, 1)
        self.lyt.addWidget(self.bottomLeftGroupBox, 2, 0)
        self.lyt.addWidget(self.bottomRightGroupBox, 2, 1)
        # 3. Show
        self.show()
        return
    
    def createBoxtime(self):
        #Groupbox for Time Settings
        self.timeBox = QGroupBox("Zeit")
        layout = QHBoxLayout()

        self.lcd_time = QLCDNumber()
        self.lcd_time.display(100)


        dial_time = QDial()
        dial_time.setValue(30)
        dial_time.setNotchesVisible(True)

        layout.addWidget(dial_time)
        layout.addWidget(self.lcd_time)
        self.timeBox.setLayout(layout)

    def createBoxVoltage(self):
        #Groupbox for Voltage Settings
        self.VoltageBox = QGroupBox("Voltage")
        layout = QHBoxLayout()

        self.lcd_voltage = QLCDNumber()
        self.lcd_voltage.display(100)


        dial_voltage = QDial()
        dial_voltage.setValue(30)
        dial_voltage.setNotchesVisible(True)

        layout.addWidget(dial_voltage)
        layout.addWidget(self.lcd_voltage)
        self.VoltageBox.setLayout(layout)

    def createBoxTrigger(self):
        #Groupbox for Voltage Settings
        self.TriggerBox = QGroupBox("Trigger")
        layout = QHBoxLayout()

        self.lcd_trigger = QLCDNumber()
        self.lcd_trigger.display(100)


        dial_trigger = QDial()
        dial_trigger.setValue(30)
        dial_trigger.setNotchesVisible(True)

        layout.addWidget(dial_trigger)
        layout.addWidget(self.lcd_trigger)
        self.TriggerBox.setLayout(layout)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Graph")

        # 2. Place the matplotlib figure
        self.myFig = MyFigureCanvas(x_len=200, y_range=[0, 100], interval=20)
        layout = QVBoxLayout()
        self.myFig.setMinimumHeight(400)
        layout.addWidget(self.myFig)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.createBoxtime()
        self.createBoxVoltage()
        self.createBoxTrigger()

        self.topRightGroupBox = QGroupBox("Einstellungen")

        layout = QVBoxLayout()
        layout.addWidget(self.timeBox)
        layout.addWidget(self.VoltageBox)
        layout.addWidget(self.TriggerBox)
        layout.addStretch(1)

        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftGroupBox(self):
        self.bottomLeftGroupBox = QGroupBox("Frequenzgenerator")

        self.lcd_amplitude = QLCDNumber()
        self.lcd_amplitude.display(100)

        self.lcd_frequenz = QLCDNumber()
        self.lcd_frequenz.display(100)

        amplitudebox = QGroupBox("Amplitude")
        frequenzbox = QGroupBox("Frequenz")
        dial_amplitude = QDial()
        dial_amplitude.setValue(30)
        dial_amplitude.setNotchesVisible(True)

        dial_frequenz = QDial()
        dial_frequenz.setValue(30)
        dial_frequenz.setNotchesVisible(True)

        layoutamp = QHBoxLayout()
        layoutamp.addWidget(dial_amplitude)
        layoutamp.addWidget(self.lcd_amplitude)
        layoutamp.addStretch(1)

        layoutfre = QHBoxLayout()
        layoutfre.addWidget(dial_frequenz)
        layoutfre.addWidget(self.lcd_frequenz)
        layoutfre.addStretch(1)

        amplitudebox.setLayout(layoutamp)
        frequenzbox.setLayout(layoutfre)


        layout = QHBoxLayout()
        layout.addWidget(amplitudebox)
        layout.addWidget(frequenzbox)

        layout.addStretch(1)

        self.bottomLeftGroupBox.setLayout(layout)


    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Input Settings")

        self.label = QLabel('Woher soll das Signal bezogen werden ?')
        self.rbtn1 = QRadioButton('Aus Datei lesen')
        self.rbtn2 = QRadioButton('generiertes Signal')
        self.rbtn3 = QRadioButton('Live Aufnahme')
        self.freelabel = QLabel("")
        self.label2 = QLabel('Soll das Signal invertiert werden?')
        self.checkBoxinv = QCheckBox("Signal invertieren")
        self.label3 = QLabel('Gerät für Live Aufnahme')
        self.Inputdevicesbox = QComboBox()
        self.Inputdevicesbox.addItems(["Audiokarte", "Mikrofon", "whatever"])
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.rbtn1)
        layout.addWidget(self.rbtn2)
        layout.addWidget(self.rbtn3)
        layout.addWidget(self.freelabel)
        layout.addWidget(self.label2)
        layout.addWidget(self.checkBoxinv)
        layout.addWidget(self.freelabel)
        layout.addWidget(self.label3)
        layout.addWidget(self.Inputdevicesbox)
        layout.addStretch(1)
        self.bottomRightGroupBox.setLayout(layout)


class MyFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''
    def __init__(self, x_len:int, y_range:List, interval:int) -> None:
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        x = list(range(0, x_len))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_  = self.figure.subplots()
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y)

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y,), interval=interval, blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        y.append(round(get_next_datapoint(), 2))     # Add new datapoint
        y = y[-self._x_len_:]                        # Truncate list _y_
        self._line_.set_ydata(y)
        return self._line_,

# Data source
# ------------
n = np.linspace(0, 499, 500)
d = 50 + 25 * (np.sin(n / 8.3)) + 10 * (np.sin(n / 7.5)) - 5 * (np.sin(n / 1.5))
i = 0
def get_next_datapoint():
    global i
    i += 1
    if i > 499:
        i = 0
    return d[i]

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    qapp.exec_()