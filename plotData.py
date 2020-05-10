import matplotlib

import matplotlib.pyplot as plt

plt.show(block=False)
plt.ion()
import matplotlib.animation as animation
import time
import numpy
from mpl_toolkits.mplot3d import Axes3D

class plotData:
    def __init__(self):
        self.fig, [[self.currentX,self.currentY,self.currentZ], [self.diffX, self.diffY, self.diffZ], [self.current3D, self.diff3D, self.predicted3D]] = plt.subplots(3, 3)

        #ax = Axes3D(self.fig)
    def subPlot(self, ax, data):
        ax.clear()
        ax.plot(*data)
    def subPlot3D(self, ax, data):
        ax.clear()
        ax.plot(*data)

    def plot(self, plotData, graphDataLengthToDisplay):
        gdl = None
        if(len(plotData['timestamp']) > graphDataLengthToDisplay):
            gdl = graphDataLengthToDisplay
        else:
            gdl = len(plotData['timestamp'])
        self.subPlot(self.currentX, [plotData['timestamp'],plotData['dobotX'],plotData['timestamp'],plotData['oculusX']])
        self.subPlot(self.currentY, [plotData['timestamp'],plotData['dobotY'],plotData['timestamp'],plotData['oculusY']])
        self.subPlot(self.currentZ, [plotData['timestamp'],plotData['dobotZ'],plotData['timestamp'],plotData['oculusZ']])

        self.subPlot(self.diffX, [plotData['timestamp'],plotData['diffX']])
        self.subPlot(self.diffY, [plotData['timestamp'],plotData['diffY']])
        self.subPlot(self.diffZ, [plotData['timestamp'],plotData['diffZ']])

        #self.subPlot3D(self.current3D, [plotData['dobotX'],plotData['dobotY'],plotData['dobotZ'],plotData['oculusX'],plotData['oculusY'],plotData['oculusZ']])
        self.subPlot(self.diff3D, [plotData['timestamp'],plotData['dobotX']])
        self.subPlot(self.predicted3D, [plotData['timestamp'],plotData['dobotX']])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.firstPlot = False

        #self.fig.canvas.draw()
        #self.fig.canvas.flush_events()
        #plt.pause(0.001)
        #self.plottingThread.start()
        #time.sleep(0.5)

