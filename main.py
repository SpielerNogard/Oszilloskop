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

from FigureCanvas import MyFigureCanvas
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


        self.dial_time = QDial()
        self.dial_time.setValue(30)
        self.dial_time.setNotchesVisible(True)
        self.dial_time.valueChanged.connect(self.dial_time_changed)

        layout.addWidget(self.dial_time)
        layout.addWidget(self.lcd_time)
        self.timeBox.setLayout(layout)

    def createBoxVoltage(self):
        #Groupbox for Voltage Settings
        self.VoltageBox = QGroupBox("Voltage")
        layout = QHBoxLayout()

        self.lcd_voltage = QLCDNumber()
        self.lcd_voltage.display(100)


        self.dial_voltage = QDial()
        self.dial_voltage.setValue(30)
        self.dial_voltage.setNotchesVisible(True)
        self.dial_voltage.valueChanged.connect(self.dial_voltage_changed)
        layout.addWidget(self.dial_voltage)
        layout.addWidget(self.lcd_voltage)
        self.VoltageBox.setLayout(layout)

    def createBoxTrigger(self):
        #Groupbox for Voltage Settings
        self.TriggerBox = QGroupBox("Trigger")
        layout = QHBoxLayout()

        self.lcd_trigger = QLCDNumber()
        self.lcd_trigger.display(100)


        self.dial_trigger = QDial()
        self.dial_trigger.setValue(30)
        self.dial_trigger.setNotchesVisible(True)
        self.dial_trigger.valueChanged.connect(self.dial_trigger_changed)

        layout.addWidget(self.dial_trigger)
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
        self.dial_amplitude = QDial()
        self.dial_amplitude.setValue(30)
        self.dial_amplitude.setNotchesVisible(True)
        self.dial_amplitude.valueChanged.connect(self.dial_amplitude_changed)

        self.dial_frequenz = QDial()
        self.dial_frequenz.setValue(30)
        self.dial_frequenz.setNotchesVisible(True)
        self.dial_frequenz.valueChanged.connect(self.dial_frequenz_changed)

        layoutamp = QHBoxLayout()
        layoutamp.addWidget(self.dial_amplitude)
        layoutamp.addWidget(self.lcd_amplitude)
        layoutamp.addStretch(1)

        layoutfre = QHBoxLayout()
        layoutfre.addWidget(self.dial_frequenz)
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
        self.rbtn1.toggled.connect(self.set_file_signal)

        self.rbtn2 = QRadioButton('generiertes Signal')
        self.rbtn2.setChecked(True)
        self.rbtn2.toggled.connect(self.set_generated_signal)

        self.rbtn3 = QRadioButton('Live Aufnahme')
        self.rbtn3.toggled.connect(self.set_live_signal)

        self.freelabel = QLabel("")
        self.label2 = QLabel('Soll das Signal invertiert werden?')
        self.checkBoxinv = QCheckBox("Signal invertieren")
        self.checkBoxinv.stateChanged.connect(self.check_inverted)

        self.label3 = QLabel('Gerät für Live Aufnahme')
        self.Inputdevicesbox = QComboBox()
        self.Inputdevicesbox.addItems(["Audiokarte", "Mikrofon", "whatever"])
        self.Inputdevicesbox.currentIndexChanged.connect(self.inputdevice_changed)

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


    def dial_time_changed(self):
        getValue = self.dial_time.value()
        self.lcd_time.display(getValue)
    
    def dial_voltage_changed(self):
        getValue = self.dial_voltage.value()
        self.lcd_voltage.display(getValue)

    def dial_trigger_changed(self):
        getValue = self.dial_trigger.value()
        self.lcd_trigger.display(getValue)
    
    def dial_amplitude_changed(self):
        getValue = self.dial_amplitude.value()
        self.lcd_amplitude.display(getValue)

    def dial_frequenz_changed(self):
        getValue = self.dial_frequenz.value()
        self.lcd_frequenz.display(getValue)

    def set_generated_signal(self):
        if self.rbtn2.isChecked():
            print("Signal ist nun generiert")
    
    def set_file_signal(self):
        if self.rbtn1.isChecked():
            print("Signal ist nun file")
    
    def set_live_signal(self):
        if self.rbtn3.isChecked():
            print("Signal ist nun live")
        
    def check_inverted(self, state):
        if state == QtCore.Qt.Checked:
            print("Signal wird invertiert")
        else:
            print("Signal wird nicht mehr invertiert")

    def inputdevice_changed(self,i):
        print("Items in the list are :")
        for count in range(self.Inputdevicesbox.count()):
            print(self.Inputdevicesbox.itemText(count))
        print("Current index",i,"selection changed ",self.Inputdevicesbox.currentText())

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    qapp.exec_()