from __future__ import annotations
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QGridLayout, QGroupBox,
                                QLabel, QRadioButton, QVBoxLayout, QWidget)

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
        self.rbtn1 = QRadioButton('Mikrofon')
        self.rbtn1.toggled.connect(self.set_mikrofon_signal)

        self.rbtn2 = QRadioButton('generiertes Signal')
        self.rbtn2.setChecked(True)
        self.rbtn2.toggled.connect(self.set_generated_signal)

        self.rbtn3 = QRadioButton('Mikrofon + generiertes Signal')
        self.rbtn3.toggled.connect(self.set_mikrofon_and_generated_signal)

        self.freelabel = QLabel("")
        self.label2 = QLabel('Soll das Signal invertiert werden?')
        self.checkBoxinv = QCheckBox("Signal invertieren")
        self.checkBoxinv.stateChanged.connect(self.check_inverted)

        self.label4 = QLabel('Generierte Signalart:')
        self.signaltypebox = QComboBox()
        self.signaltypebox.addItems(["Sinus","Sawtooth","Square"])
        self.signaltypebox.currentIndexChanged.connect(self.signaltype_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.rbtn1)
        layout.addWidget(self.rbtn2)
        layout.addWidget(self.rbtn3)
        layout.addWidget(self.freelabel)
        layout.addWidget(self.label2)
        layout.addWidget(self.checkBoxinv)
        layout.addWidget(self.freelabel)

        layout.addWidget(self.label4)
        layout.addWidget(self.signaltypebox)
        layout.addStretch(1)
        self.bottomRightGroupBox.setLayout(layout)

    def set_generated_signal(self):
        if self.rbtn2.isChecked():
            self.myFig.set_generated_signal()

    def set_mikrofon_signal(self):
        if self.rbtn1.isChecked():
            self.myFig.set_mikrofon()
    def set_mikrofon_and_generated_signal(self):
        if self.rbtn3.isChecked():
            self.myFig.set_mikrofon_and_generated()
    def check_inverted(self, state):
        if state == QtCore.Qt.Checked:
            self.myFig.set_inverted(True)
        else:
            self.myFig.set_inverted(False)

    def signaltype_changed(self, i):
        self.Signalgenerator.signal_to_generate = self.signaltypebox.currentText()
