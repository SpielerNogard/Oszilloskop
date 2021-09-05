from __future__ import annotations
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import numpy as np
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
        interval = 33

        self.start_frequenz = 0
        self.stop_frequenz = 20000

        FigureCanvas.__init__(self, mpl_fig.Figure())

        self._ax_ = self.figure.subplots()
        self._ax_.set_ylim(ymin=0, ymax=5)
        self._ax_.set_xlim(xmin=self.start_frequenz, xmax=self.stop_frequenz)
        self._line_, = self._ax_.plot(self.myFig.x, self.myFig.current_data_showing)

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, interval=interval, blit=False)
        return

    def _update_canvas_(self, i) -> None:
        '''
        This function gets called regularly by the timer.

        '''

        y = []
        x = self.myFig.x
        if self.myFig.screen_filled:
            y = self.myFig.current_data_showing
        else:
            y = self.myFig.all_data
        x = self.myFig.x

        self._ax_.set_ylim(ymin=0, ymax= self.myFig.voltage_per_box * self.myFig.number_of_boxes / 2)

        # Number of sample points
        N = len(x)

        # sample spacing
        T = 1/ self.myFig.abtastrate

        # Frequenzen und Frequenzintervalle von scipy berechnen lassen
        yf = fft(y)[0:N // 2]
        xf = fftfreq(N, T)[:N // 2]
        self._line_.set_data(xf, 2.0 / N * np.abs(yf))
        return

    def set_start_frequenz(self, frequenz):
        self.start_frequenz = frequenz
        self._ax_.set_xlim(xmin=self.start_frequenz, xmax=self.stop_frequenz)

    def set_stop_frequenz(self, frequenz):
        self.stop_frequenz = frequenz
        self._ax_.set_xlim(xmin=self.start_frequenz, xmax=self.stop_frequenz)