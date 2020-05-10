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
        self.fig2D, [[self.currentX,self.currentY,self.currentZ], [self.diffX, self.diffY, self.diffZ]] = plt.subplots(2, 3, sharex=True)
        self.fig3D = plt.figure(figsize=(4, 8))
        self.current3D = self.fig3D.add_subplot(311, projection='3d')
        self.diff3D = self.fig3D.add_subplot(312, projection='3d')
        self.predicted3D = self.fig3D.add_subplot(313, projection='3d')

        # handles, labels = ax.get_legend_handles_labels()
        # title = 'Nyquist graph cmd: ' + str(cmdUsed) + " \nFrom " + str(start) + " took: " + str(
        #     "{:.2f}".format(took)) + " s"
        # ax.set_title(title)
        # ax.set_xlabel('Z_Re [Ohms]')
        # ax.set_ylabel('Z_Im [Ohms]')
        #
        # plt.legend(handles, labels, bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 6})

        #ax = Axes3D(self.fig)
    def subPlot(self, ax, data, color = None):
        ax.clear()
        if color is None:
            ax.plot(*data)
        else:
            ax.plot(*data,color)

    def subClear(self):
        self.currentX.clear()
        self.currentY.clear()
        self.currentZ.clear()
        self.diffX.clear()
        self.diffY.clear()
        self.diffZ.clear()
        self.current3D.clear()
        self.diff3D.clear()
        self.predicted3D.clear()

    def subLegend(self):
        self.currentX.legend(['ARM','VR'],prop={"size":6})
        self.diffX.xaxis.set_label_coords(1.05, -0.025)
        self.diffY.xaxis.set_label_coords(1.05, -0.025)
        self.diffZ.xaxis.set_label_coords(1.05, -0.025)

        self.currentX.set_ylabel('[mm]')
        self.diffX.set_ylabel('[mm]')
        self.diffX.set_xlabel('[s]')
        self.diffY.set_xlabel('[s]')
        self.diffZ.set_xlabel('[s]')

        # Put a legend below current axis
        self.currentY.legend(['ARM','VR'],prop={"size":6})
        #self.currentY.set_zlabel('[mm]')
        self.currentZ.legend(['ARM','VR'],prop={"size":6})
        self.current3D.legend(['ARM','VR'],prop={"size":6})

        self.current3D.set_xlabel('[mm]')
        self.current3D.set_ylabel('[mm]')
        self.current3D.set_zlabel('[mm]')

        self.diff3D.set_xlabel('[mm]')
        self.diff3D.set_ylabel('[mm]')
        self.diff3D.set_zlabel('[mm]')

        self.predicted3D.set_xlabel('[mm]')
        self.predicted3D.set_ylabel('[mm]')
        self.predicted3D.set_zlabel('[mm]')

    def plot_figures(figures, nrows=1, ncols=1):
        """Plot a dictionary of figures.

        Parameters
        ----------
        figures : <title, figure> dictionary
        ncols : number of columns of subplots wanted in the display
        nrows : number of rows of subplots wanted in the figure
        """

        fig, axeslist = plt.subplots(ncols=ncols, nrows=nrows)
        for ind, title in enumerate(figures):
            axeslist.ravel()[ind].imshow(figures[title], cmap=plt.gray())
            axeslist.ravel()[ind].set_title(title)
            axeslist.ravel()[ind].set_axis_off()
        plt.tight_layout()  # optional

    def plot(self, plotData, graphDataLengthToDisplay):
        gdl = None
        if(len(plotData['timestamp']) > graphDataLengthToDisplay):
            gdl = graphDataLengthToDisplay
        else:
            gdl = len(plotData['timestamp'])
        self.subClear()
        self.currentX.plot(plotData['timestamp'],plotData['dobotX'],plotData['timestamp'],plotData['oculusX'])
        self.currentY.plot(plotData['timestamp'],plotData['dobotY'],plotData['timestamp'],plotData['oculusY'])
        self.currentZ.plot(plotData['timestamp'],plotData['dobotZ'],plotData['timestamp'],plotData['oculusZ'])

        self.diffX.plot(plotData['timestamp'],plotData['diffX'],color = 'g')
        self.diffY.plot(plotData['timestamp'],plotData['diffY'],color = 'g')
        self.diffZ.plot(plotData['timestamp'],plotData['diffZ'],color = 'g')

        self.current3D.plot(plotData['dobotX'],plotData['dobotY'],plotData['dobotZ'],plotData['oculusX'],plotData['oculusY'],plotData['oculusZ'])
        self.diff3D.plot(plotData['diffX'],plotData['diffY'],plotData['diffZ'],color = 'g')
        self.predicted3D.plot(plotData['diffX'],plotData['diffY'],plotData['diffZ'],color = 'g')

        self.currentX.set_title('Current X')
        self.currentY.set_title('Current Y')
        self.currentZ.set_title('Current Z')

        self.diffX.set_title('Diff X')
        self.diffY.set_title('Diff Y')
        self.diffZ.set_title('Diff Z')

        self.current3D.set_title('Current 3D')
        self.diff3D.set_title('Diff 3D')
        self.predicted3D.set_title('Diff 3D')

        self.subLegend()
        self.fig2D.canvas.draw()
        self.fig2D.canvas.flush_events()
        plt.get_current_fig_manager().window.wm_geometry("+1000+100")
        self.fig3D.canvas.draw()
        self.fig3D.canvas.flush_events()
        self.firstPlot = False

        #self.fig.canvas.draw()
        #self.fig.canvas.flush_events()
        #plt.pause(0.001)
        #self.plottingThread.start()
        #time.sleep(0.5)

