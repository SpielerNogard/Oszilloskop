from __future__ import annotations
import sys
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from PyQt5.QtWidgets import (QDial, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
        QVBoxLayout,QLCDNumber)


from FigureCanvas import MyFigureCanvas
from Signalgenerator import SignalGenerator
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from Settings import Settingswindow
from FrequenzWindow import FrequenzWindow
from Frequenzanalyse import Frequenzcanvas
import math
class Oszilloskop(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.SignalGenerator = SignalGenerator()
        self.myFig = MyFigureCanvas(self.SignalGenerator)
        self.myFigfre = Frequenzcanvas(self.myFig)
        self.settings = Settingswindow(self.SignalGenerator,self.myFig)
        self.FreqWindow = FrequenzWindow(self.myFigfre,self.myFig)
        self.create_labels()
        self.window_settings()
        self.add_windows()
        self.add_functions()
        self.createMenuBar()

        self.show()

    def window_settings(self):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("Oszilloskop")
        self.frm = QtWidgets.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: #eeeeec; }")
        self.lyt = QGridLayout()
        self.frm.setLayout(self.lyt)
        self.setCentralWidget(self.frm)

    def show_Settings(self):
        self.settings.show()

    def show_freq_analyse(self):
        self.FreqWindow.show()

    def createMenuBar(self):
        SettingsAct = QAction(QIcon('settings.png'), '&Settingswindow', self)
        SettingsAct.setStatusTip('Opens Settings')
        SettingsAct.triggered.connect(self.show_Settings)

        freqact = QAction(QIcon('settings.png'), '&Frequenzanalyse', self)
        freqact.setStatusTip('Opens Frequenzanalyse')
        freqact.triggered.connect(self.show_freq_analyse)


        self.statusBar()

        menubar = self.menuBar()
        settingsmenu = menubar.addMenu('&Settings')
        settingsmenu.addAction(SettingsAct)

        freqmenu = menubar.addMenu('&Frequenzanalyse')
        freqmenu.addAction(freqact)

    def add_windows(self):
        self.createTopLeftGroupBox()
        self.lyt.addWidget(self.topLeftGroupBox, 1, 0)

        self.createBottomLeftGroupBox()
        self.lyt.addWidget(self.bottomLeftGroupBox, 2, 0)

        self.createTopRightGroupBox()
        self.lyt.addWidget(self.topRightGroupBox, 1, 1)

        self.create_bottonḾmost_right_box()
        self.lyt.addWidget(self.graphpositionbox, 2, 1)

    def add_functions(self):
        self.dial_amplitude.valueChanged.connect(self.dial_amplitude_changed)
        self.dial_frequenz.valueChanged.connect(self.dial_frequenz_changed)
        self.dial_time.valueChanged.connect(self.dial_time_changed)
        self.dial_voltage.valueChanged.connect(self.dial_voltage_changed)
        self.dial_trigger.valueChanged.connect(self.dial_trigger_changed)
        self.dial_pos_x.valueChanged.connect(self.dial_posx_changed)
        self.dial_pos_y.valueChanged.connect(self.dial_posy_changed)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Graph")

        # 2. Place the matplotlib figure
        
        layout = QVBoxLayout()
        self.myFig.setMinimumHeight(400)
        layout.addWidget(self.myFig)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def create_labels(self):
        self.label_amp = QLabel()
        self.label_amp.setText("V")

        self.label_frequenzg = QLabel()
        self.label_frequenzg.setText("Hz")

        self.label_time = QLabel()
        self.label_time.setText("ms")

        self.label_voltage = QLabel()
        self.label_voltage.setText("V")

        self.label_trigger = QLabel()
        self.label_trigger.setText("%")
        
        self.label_posx = QLabel()
        self.label_posx.setText("%")

        self.label_posy = QLabel()
        self.label_posy.setText("%")
    def createBottomLeftGroupBox(self):
        self.bottomLeftGroupBox = QGroupBox("Frequenzgenerator")

        self.lcd_amplitude = QLCDNumber()
        self.lcd_amplitude.display(0.1)
        
        self.lcd_frequenz = QLCDNumber()
        self.lcd_frequenz.display(20)

        amplitudebox = QGroupBox("Amplitude")
        frequenzbox = QGroupBox("Frequenz")

        self.dial_amplitude = QDial()
        self.dial_amplitude.setValue(1)
        self.dial_amplitude.setRange(0,10)
        self.dial_amplitude.setNotchesVisible(True)


        self.dial_frequenz = QDial()
        self.dial_frequenz.setValue(0)
        self.dial_frequenz.setRange(-2, 13)      # 20 - 20.000 Hz
        self.dial_frequenz.setNotchesVisible(True)


        layoutamp = QHBoxLayout()
        layoutamp.addWidget(self.dial_amplitude)
        layoutamp.addWidget(self.lcd_amplitude)
        layoutamp.addWidget(self.label_amp)
        #layoutamp.addWidget(vbox)
        layoutamp.addStretch(1)

        layoutfre = QHBoxLayout()
        layoutfre.addWidget(self.dial_frequenz)
        layoutfre.addWidget(self.lcd_frequenz)
        layoutfre.addWidget(self.label_frequenzg)
        layoutfre.addStretch(1)

        amplitudebox.setLayout(layoutamp)
        frequenzbox.setLayout(layoutfre)


        layout = QHBoxLayout()
        layout.addWidget(amplitudebox)
        layout.addWidget(frequenzbox)

        layout.addStretch(1)

        self.bottomLeftGroupBox.setLayout(layout)

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

    def createBoxtime(self):
        #Groupbox for Time Settings
        self.timeBox = QGroupBox("Zeit")
        layout = QHBoxLayout()

        self.lcd_time = QLCDNumber()
        self.lcd_time.display(10)


        self.dial_time = QDial()
        self.dial_time.setRange(-15, 0)  # 0.01 ms bis 1000ms (für insgesamt 10 Sekunden Aufnahme)
        self.dial_time.setValue(-6)  # 10 ms
        self.dial_time.setNotchesVisible(True)
        

        layout.addWidget(self.dial_time)
        layout.addWidget(self.lcd_time)
        layout.addWidget(self.label_time)
        self.timeBox.setLayout(layout)

    def createBoxVoltage(self):
        #Groupbox for Voltage Settings
        self.VoltageBox = QGroupBox("Voltage")
        layout = QHBoxLayout()

        self.lcd_voltage = QLCDNumber()
        self.lcd_voltage.display(0.1)


        self.dial_voltage = QDial()
        self.dial_voltage.setValue(1)
        self.dial_voltage.setRange(1,10)
        self.dial_voltage.setNotchesVisible(True)
        
        layout.addWidget(self.dial_voltage)
        layout.addWidget(self.lcd_voltage)
        layout.addWidget(self.label_voltage)
        self.VoltageBox.setLayout(layout)

    def createBoxTrigger(self):
        #Groupbox for Voltage Settings
        self.TriggerBox = QGroupBox("Trigger")
        layout = QHBoxLayout()

        self.lcd_trigger = QLCDNumber()
        self.lcd_trigger.display(0)


        self.dial_trigger = QDial()
        self.dial_trigger.setValue(0)
        self.dial_trigger.setNotchesVisible(True)
        

        layout.addWidget(self.dial_trigger)
        layout.addWidget(self.lcd_trigger)
        layout.addWidget(self.label_trigger)
        self.TriggerBox.setLayout(layout)

    def create_bottonḾmost_right_box(self):
        self.graphpositionbox = QGroupBox("GraphPositionnierung")

        self.lcd_posx = QLCDNumber()
        self.lcd_posx.display(0)

        self.lcd_posy = QLCDNumber()
        self.lcd_posy.display(0)

        x_box = QGroupBox("X Position")
        y_box = QGroupBox("Y Position")
        self.dial_pos_x = QDial()
        self.dial_pos_x.setValue(50)
        self.dial_pos_x.setNotchesVisible(True)
        

        self.dial_pos_y = QDial()
        self.dial_pos_y.setValue(50)
        self.dial_pos_y.setNotchesVisible(True)
        

        layoutx= QHBoxLayout()
        layoutx.addWidget(self.dial_pos_x)
        layoutx.addWidget(self.lcd_posx)
        layoutx.addWidget(self.label_posx)
        layoutx.addStretch(1)

        layouty = QHBoxLayout()
        layouty.addWidget(self.dial_pos_y)
        layouty.addWidget(self.lcd_posy)
        layouty.addWidget(self.label_posy)
        layouty.addStretch(1)

        x_box.setLayout(layoutx)
        y_box.setLayout(layouty)


        layout = QHBoxLayout()
        layout.addWidget(x_box)
        layout.addWidget(y_box)

        layout.addStretch(1)

        self.graphpositionbox.setLayout(layout)

    def dial_time_changed(self):
        getValue = self.dial_time.value()
        wert = self.give_me_exponential(getValue)

        self.lcd_time.display(wert * 1000)
        self.myFig.set_time(wert)
    
    def dial_voltage_changed(self):
        getValue = self.dial_voltage.value() * 0.1
        self.lcd_voltage.display(getValue)
        self.myFig.set_voltage(getValue)

    def dial_trigger_changed(self):
        getValue = self.dial_trigger.value()
        self.lcd_trigger.display(getValue)
        self.myFig.set_trigger(getValue)

    def dial_amplitude_changed(self):
        getValue = self.dial_amplitude.value() * 0.1
        self.lcd_amplitude.display(getValue)
        self.myFig.set_amplitude(getValue)

    def dial_frequenz_changed(self):
        getValue = self.dial_frequenz.value()
        wert = self.give_me_exponential(getValue)

        self.lcd_frequenz.display(wert)
        self.myFig.set_frequenz(wert)

    def dial_posx_changed(self):
        getValue = self.dial_pos_x.value()
        self.lcd_posx.display(getValue)
        self.myFig.set_posx(getValue)

    def dial_posy_changed(self):
        getValue = self.dial_pos_y.value()
        self.lcd_posy.display(getValue)
        self.myFig.set_posy(getValue)

    def give_me_exponential(self,i):
        wert = 1
        if i%3 == 1:
            wert = 2
        if i%3 == 2:
            wert = 5

        power_of_ten = math.floor(i/3)
        wert = wert * math.pow(10, power_of_ten)
        return wert

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = Oszilloskop()
    qapp.exec_()

