from __future__ import annotations
from PyQt5.QtWidgets import (QDial, QGridLayout, QGroupBox, QHBoxLayout, QLabel,QVBoxLayout, QWidget,QLCDNumber)

import math
class FrequenzWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self,myfig,real_my_fig):
        super().__init__()
        self.mygraph = real_my_fig
        self.myFigfre = myfig
        self.setWindowTitle("Frequenzanalyse")
        self.lyt = QGridLayout()
        self.create_labels()
        self.create_Frequenzbox()
        self.createFreqSettings()
        self.lyt.addWidget(self.freqbox, 1, 0)
        self.lyt.addWidget(self.topRightGroupBox, 1, 1)
        self.setLayout(self.lyt)

    def create_labels(self):
        self.label_freqstart = QLabel()
        self.label_freqstart.setText("Hz")

        self.label_freqstop = QLabel()
        self.label_freqstop.setText("Hz")

    def create_Frequenzbox(self):
        self.freqbox = QGroupBox("Frequenzanalyse")

        # 2. Place the matplotlib figure
        
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
        self.lcd_start.display(20)


        self.dial_start = QDial()
        self.dial_start.setValue(0)
        self.dial_start.setRange(-2, 14)  # 20 - 20.000 Hz
        self.dial_start.setNotchesVisible(True)
        self.dial_start.valueChanged.connect(self.dial_start_changed)

        layout.addWidget(self.dial_start)
        layout.addWidget(self.lcd_start)
        layout.addWidget(self.label_freqstart)
        self.boxfreqstart.setLayout(layout) 

    def createBoxfreqstop(self):
        #Groupbox for Time Settings
        self.boxfreqstop = QGroupBox("Frequenz Stop")
        layout = QHBoxLayout()

        self.lcd_stop = QLCDNumber()
        self.lcd_stop.display(20000)

        self.dial_stop = QDial()
        self.dial_stop.setValue(13)
        self.dial_stop.setRange(-2, 14)      # 20 - 20.000 Hz
        self.dial_stop.setNotchesVisible(True)
        self.dial_stop.valueChanged.connect(self.dial_stop_changed)

        layout.addWidget(self.dial_stop)
        layout.addWidget(self.lcd_stop)
        layout.addWidget(self.label_freqstop)
        self.boxfreqstop.setLayout(layout) 

    def dial_start_changed(self):
        getValue = self.dial_start.value()
        stop_value = self.dial_stop.value()

        if getValue >= stop_value:
            getValue = stop_value - 1
            self.dial_start.setValue(getValue)

        wert = self.give_me_exponential(getValue)
        self.lcd_start.display(wert)
        self.myFigfre.set_start_frequenz(wert)
    
    def dial_stop_changed(self):
        getValue = self.dial_stop.value()
        start_value = self.dial_start.value()
        if getValue <= start_value:
            getValue = start_value + 1
            self.dial_stop.setValue(getValue)

        wert = self.give_me_exponential(getValue)
        self.lcd_stop.display(wert)
        self.myFigfre.set_stop_frequenz(wert)

    def give_me_exponential(self,i):
        wert = 1
        if i%3 == 1:
            wert = 2
        if i%3 == 2:
            wert = 5

        power_of_ten = math.floor(i/3)
        wert = wert * math.pow(10, power_of_ten)
        return wert