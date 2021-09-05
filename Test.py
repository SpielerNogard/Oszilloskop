from __future__ import annotations

import numpy
from matplotlib.backends.backend_qt5agg import FigureCanvas

import matplotlib.figure as mpl_fig
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np

import time
import threading
import pyaudio

def Main():
    print(np.sin(2*np.pi *20000 * 2.0/44100) -np.sin(2*np.pi *20000 * 3.0/44100) )

if __name__ == "__main__":
    Main()

