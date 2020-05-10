import matplotlib
import matplotlib.pyplot as plt
plt.ion()
import matplotlib.animation as animation
import time
import numpy

class plotData:
    def __init__(self):
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.xArray = []
        self.yArray = []

    def animate(self):
        self.ax1.clear()
        self.ax1.plot(self.xArray, self.yArray)

    def plot(self, xArray, yArray):
        self.xArray = xArray
        self.yArray = yArray
        self.animate()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        #self.plottingThread.start()
        #time.sleep(0.5)

