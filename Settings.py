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

class Settingswindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self,Signalgenerator,fig):
        super().__init__()
        self.myFig = fig
        self.setWindowTitle("Settings")
        self.lyt = QGridLayout()
        self.createBottomRightGroupBox()
        self.lyt.addWidget(self.bottomRightGroupBox, 1, 0)
        self.setLayout(self.lyt)

        self.Signalgenerator = Signalgenerator

    

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Input Settings")

        self.label = QLabel('Woher soll das Signal bezogen werden ?')
        self.rbtn1 = QRadioButton('Aus Datei lesen')
        self.rbtn1.toggled.connect(self.set_file_signal)

        self.rbtn2 = QRadioButton('generiertes Signal')
        self.rbtn2.setChecked(True)
        self.rbtn2.toggled.connect(self.set_generated_signal)

        

        self.freelabel = QLabel("")
        self.label2 = QLabel('Soll das Signal invertiert werden?')
        self.checkBoxinv = QCheckBox("Signal invertieren")
        self.checkBoxinv.stateChanged.connect(self.check_inverted)

        self.label3 = QLabel('Gerät für Live Aufnahme')
        self.Inputdevicesbox = QComboBox()
        self.Inputdevicesbox.addItems(["Audiokarte", "Mikrofon", "whatever"])
        self.Inputdevicesbox.currentIndexChanged.connect(self.inputdevice_changed)

        self.label4 = QLabel('Generierte Signalart:')
        self.signaltypebox = QComboBox()
        self.signaltypebox.addItems(["Sinus","Sawtooth","Square"])
        self.signaltypebox.currentIndexChanged.connect(self.signaltype_changed)


        layout = QVBoxLayout()
        layout.addWidget(self.label)
        #layout.addWidget(self.rbtn1)
        layout.addWidget(self.rbtn2)
        layout.addWidget(self.freelabel)
        layout.addWidget(self.label2)
        layout.addWidget(self.checkBoxinv)
        layout.addWidget(self.freelabel)
        #layout.addWidget(self.label3)
        #layout.addWidget(self.Inputdevicesbox)
        layout.addWidget(self.label4)
        layout.addWidget(self.signaltypebox)
        layout.addStretch(1)
        self.bottomRightGroupBox.setLayout(layout)

    def set_generated_signal(self):
        if self.rbtn2.isChecked():
            print("Signal ist nun generiert")
            self.myFig.set_generated_signal()
    def set_file_signal(self):
        if self.rbtn1.isChecked():
            print("Signal ist nun file")
            self.myFig.set_file_signal()
    
    def check_inverted(self, state):
        if state == QtCore.Qt.Checked:
            print("Signal wird invertiert")
            self.myFig.set_inverted(True)
        else:
            print("Signal wird nicht mehr invertiert")
            self.myFig.set_inverted(False)
            
    def inputdevice_changed(self,i):
        print("Items in the list are :")
        for count in range(self.Inputdevicesbox.count()):
            print(self.Inputdevicesbox.itemText(count))
        print("Current index",i,"selection changed ",self.Inputdevicesbox.currentText())

    def signaltype_changed(self, i):
        self.Signalgenerator.signal_to_generate = self.signaltypebox.currentText()
        print("Items in the list are :")
        for count in range(self.signaltypebox.count()):
            print(self.signaltypebox.itemText(count))
        print("Current index",i,"selection changed ",self.signaltypebox.currentText())

