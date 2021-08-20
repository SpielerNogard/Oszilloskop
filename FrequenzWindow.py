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


from Frequenzanalyse import Frequenzcanvas

class FrequenzWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Frequenzanalyse")
        self.lyt = QGridLayout()
        self.create_Frequenzbox()
        self.createFreqSettings()
        self.lyt.addWidget(self.freqbox, 1, 0)
        self.lyt.addWidget(self.topRightGroupBox, 1, 1)
        self.setLayout(self.lyt)
        #self.show()

    def create_Frequenzbox(self):
        self.freqbox = QGroupBox("Frequenzanalyse")

        # 2. Place the matplotlib figure
        self.myFigfre = Frequenzcanvas()
        layout = QVBoxLayout()
        self.myFigfre.setMinimumHeight(400)
        layout.addWidget(self.myFigfre)
        layout.addStretch(1)
        self.freqbox.setLayout(layout)

    def createFreqSettings(self):
        self.createBoxfreqstart()
        self.createBoxfreqstop()

        self.topRightGroupBox = QGroupBox("Einstellungen")

        layout = QVBoxLayout()
        layout.addWidget(self.boxfreqstart)
        layout.addWidget(self.boxfreqstop)
        layout.addStretch(1)

        self.topRightGroupBox.setLayout(layout)

    def createBoxfreqstart(self):
        #Groupbox for Time Settings
        self.boxfreqstart = QGroupBox("Frequenz Start")
        layout = QHBoxLayout()

        self.lcd_start = QLCDNumber()
        self.lcd_start.display(100)


        self.dial_start = QDial()
        self.dial_start.setValue(30)
        self.dial_start.setNotchesVisible(True)
        self.dial_start.valueChanged.connect(self.dial_start_changed)

        layout.addWidget(self.dial_start)
        layout.addWidget(self.lcd_start)
        self.boxfreqstart.setLayout(layout) 

    def createBoxfreqstop(self):
        #Groupbox for Time Settings
        self.boxfreqstop = QGroupBox("Frequenz Stop")
        layout = QHBoxLayout()

        self.lcd_stop = QLCDNumber()
        self.lcd_stop.display(100)


        self.dial_stop = QDial()
        self.dial_stop.setValue(30)
        self.dial_stop.setNotchesVisible(True)
        self.dial_stop.valueChanged.connect(self.dial_stop_changed)

        layout.addWidget(self.dial_stop)
        layout.addWidget(self.lcd_stop)
        self.boxfreqstop.setLayout(layout) 

    def dial_start_changed(self):
        getValue = self.dial_start.value()
        self.lcd_start.display(getValue)
    
    def dial_stop_changed(self):
        getValue = self.dial_stop.value()
        self.lcd_stop.display(getValue)