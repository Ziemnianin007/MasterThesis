import dobotHandler
import oculusQuestConnection
import pprint
import plotData
import fileOperation
import polynomialPrediction
import matplotlib.pyplot as plt
import time
import threading
import neuralNetworkPrediction

class coordinateOperation:
    def __init__(self, graphDataLength = 50, plot = True, save = True):
        #home dobot magician in dobotstudio, then disconnect and run

        self.dobotHandlerInstance = dobotHandler.dobotHandler()
        self.oculusQuestConnectionInstance = oculusQuestConnection.oculusQuestConnection()
        self.minZ = -115
        self.recording = False

        self.rightXLastDobot = 0
        self.rightYLastDobot = 0
        self.rightZLastDobot = 0
        self.positionArray = {}
        self.positionArray['oculusX'] = []
        self.positionArray['oculusY'] = []
        self.positionArray['oculusZ'] = []

        self.positionArray['dobotX'] = []
        self.positionArray['dobotY'] = []
        self.positionArray['dobotZ'] = []

        self.positionArray['diffX'] = []
        self.positionArray['diffY'] = []
        self.positionArray['diffZ'] = []

        self.positionArray['predictionX'] = []
        self.positionArray['predictionY'] = []
        self.positionArray['predictionZ'] = []

        self.positionArray['timestamp'] = []
        self.positionArray['oculusTimeStamp'] = []

        self.positionArray['oculusXSynchronized'] = []
        self.positionArray['oculusYSynchronized'] = []
        self.positionArray['oculusZSynchronized'] = []

        self.grip = False
        self.oldGrip = False
        self.actualPositionOculus = None
        self.oculusRefreshingThread = threading.Thread(target=self.refreshActualPosition, daemon=True)
        self.oculusRefreshingThread.start()
        time.sleep(0.25)
        self.getActualPosition()
        self.dobotPositionTimeStamp = None
        self.plotDataInstance = plotData.plotData()
        self.graphDataLength = graphDataLength
        self.plot = plot
        self.save = save
        self.polynomialPredictionInstance = polynomialPrediction.polynomalPrediction()
        time.sleep(0.25)


        #self.neuralNetworkPredictionInstance = neuralNetworkPrediction.neuralNetworkPrediction()

    #x Min -135  Max 328    av 96.5     +- 231.5
    #y Min -328 Max 328     av 0        +- 328
    #z Min -30 Max 160      av 65       +- 95
    #R Min -150 Max 150     av 0        +- 150

    """
    #position, rotation, velocity, angular velocity
    # X left
    # Y Up
    # Z Forward
    """

    def refreshActualPosition(self):
        #print("aaa")
        self.actualPositionOculus = self.oculusQuestConnectionInstance.getPosition()
        self.oldGrip = self.grip
        self.grip = self.oculusQuestConnectionInstance.getRightControllerGrip()
        self.oculusHomePosition()
        while (True):
            self.actualPositionOculus = self.oculusQuestConnectionInstance.getPosition()
            self.oldGrip = self.grip
            self.grip = self.oculusQuestConnectionInstance.getRightControllerGrip()
            self.getActualPosition()
            self.coordinateFromOculusToDobotTranslation()

            if self.recording is True:
                self.positionArray['oculusX'].append(self.oculusX)
                self.positionArray['oculusY'].append(self.oculusY)
                self.positionArray['oculusZ'].append(self.oculusZ)
                self.positionArray['oculusTimeStamp'].append(time.time())
            time.sleep(0.05)


            #print(self.actualPositionOculus)

    def oculusHomePosition(self):
        homePosition = self.actualPositionOculus
        self.homeX = homePosition[0][3]
        self.homeY = homePosition[2][3]
        self.homeZ = homePosition[1][3]

        return(self.homeX,self.homeY,self.homeZ)

    def getActualPosition(self):
        position = self.actualPositionOculus
        self.rightX = position[0][3] - self.homeX  # +- 0.25
        self.rightY = position[2][3] - self.homeY  # += 0.25
        self.rightZ = position[1][3] - self.homeZ  # +0.5 -0.1

    # def relativeHome(self,x,y,z):
    #     homePosition[0][3] = homePosition[0][3] - (x - oldPosition[0]) #+- 0.25
    #     homePosition[2][3] = homePosition[2][3] - (y - oldPosition[1]) #+= 0.25
    #     homePosition[1][3] = homePosition[1][3] - (z - oldPosition[2]) # +0.5 -0.1

    def dobotHome(self):
        self.dobotHandlerInstance.setPosition(259.1198, 0, -8.5687) #going to dobot home
        self.rightXLastDobot = 0
        self.rightYLastDobot = 0
        self.rightZLastDobot = 0
        self.positionArray = {}
        self.positionArray['oculusX'] = []
        self.positionArray['oculusY'] = []
        self.positionArray['oculusZ'] = []

        self.positionArray['dobotX'] = []
        self.positionArray['dobotY'] = []
        self.positionArray['dobotZ'] = []

        self.positionArray['diffX'] = []
        self.positionArray['diffY'] = []
        self.positionArray['diffZ'] = []

        self.positionArray['predictionX'] = []
        self.positionArray['predictionY'] = []
        self.positionArray['predictionZ'] = []

        self.positionArray['oculusXSynchronized'] = []
        self.positionArray['oculusYSynchronized'] = []
        self.positionArray['oculusZSynchronized'] = []

        self.positionArray['timestamp'] = []
        self.positionArray['oculusTimeStamp'] = []

    def coordinateFromOculusToDobotTranslation(self):

        #self.dobotX = -self.rightY / 0.25 * 231.5 + 259.1198
        #self.dobotY = -self.rightX / 0.25 * 328 + 0
        #self.dobotZ = self.rightZ / 0.25 * 150 + 0 - 8.5687
        self.oculusX = -self.rightY *1000 + 259.1198
        self.oculusY = -self.rightX *1000 + 0
        self.oculusZ = self.rightZ *1000 + 0 - 8.5687
        self.dobotX = self.oculusX
        self.dobotY = self.oculusY
        self.dobotZ = self.oculusZ
        if self.dobotZ < self.minZ:    #avoid ground contact
            self.dobotZ = self.minZ
        self.rightXLastDobot = self.rightX
        self.rightYLastDobot = self.rightY
        self.rightZLastDobot = self.rightZ

    def rebaseOculusToDobotCoordinates(self):
        self.homeX = self.homeX + (self.rightX - self.rightXLastDobot)
        self.homeY = self.homeY + (self.rightY - self.rightYLastDobot)
        self.homeZ = self.homeZ + (self.rightZ - self.rightZLastDobot)

    def moveDobotToPreparedPosition(self):
        if self.dobotZ < self.minZ:    #avoid ground contact
            self.dobotZ = self.minZ
        dobotX, dobotY, dobotZ = self.dobotX, self.dobotY, self.dobotZ
        self.dobotPositionTimeStamp = self.dobotHandlerInstance.setPosition(self.dobotX, self.dobotY, self.dobotZ)
        self.postionArrayAddDobotAndOculusPositions(dobotX, dobotY, dobotZ)

        print("X: %0.3f " % self.rightX, "Y: %0.3f " % self.rightY, "Z: %0.3f " % self.rightZ, " g: ", self.grip,
              " Prediction X: %0.3f " % self.positionArray['predictionX'][-1], "Y: %0.3f " % self.positionArray['predictionY'][-1], "Z: %0.3f " % self.positionArray['predictionZ'][-1],
              " Now: X: %0.3f " % self.positionArray['dobotX'][-1], "Y: %0.3f " % self.positionArray['dobotY'][-1], "Z: %0.3f " % self.positionArray['dobotZ'][-1])

    def moveDobotCloserToPreparedPosition(self,maxMove = 30):
        if self.dobotZ < self.minZ:    #avoid ground contact
            self.dobotZ = self.minZ
        dobotX, dobotY, dobotZ = self.dobotX, self.dobotY, self.dobotZ
        self.dobotPositionTimeStamp =self.dobotHandlerInstance.closerToPosition(self.dobotX, self.dobotY, self.dobotZ, maxMove)
        self.postionArrayAddDobotAndOculusPositions(dobotX, dobotY, dobotZ)

    def postionArrayAddDobotAndOculusPositions(self, dobotX, dobotY, dobotZ):

        self.positionArray['dobotX'].append(self.dobotPositionTimeStamp[0][0])
        self.positionArray['dobotY'].append(self.dobotPositionTimeStamp[0][1])
        self.positionArray['dobotZ'].append(self.dobotPositionTimeStamp[0][2])

        self.positionArray['predictionX'].append(dobotX)
        self.positionArray['predictionY'].append(dobotY)
        self.positionArray['predictionZ'].append(dobotZ)

        self.positionArray['oculusXSynchronized'].append(self.oculusX)
        self.positionArray['oculusYSynchronized'].append(self.oculusY)
        self.positionArray['oculusZSynchronized'].append(self.oculusZ)

        self.positionArray['diffX'].append(self.positionArray['oculusX'][-1] - self.positionArray['dobotX'][-1])
        self.positionArray['diffY'].append(self.positionArray['oculusY'][-1] - self.positionArray['dobotY'][-1])
        self.positionArray['diffZ'].append(self.positionArray['oculusZ'][-1] - self.positionArray['dobotZ'][-1])

        self.positionArray['timestamp'].append(self.dobotPositionTimeStamp[1])

        if self.save is True:
            fileOperation.saveToFolder(self.positionArray, path = self.path, silent = True)

        if self.plot is True:
            self.plotDataInstance.plot(self.positionArray, self.graphDataLength)
        #pprint.pprint(self.positionArray)

    def loadData(self):
        self.positionArray = fileOperation.loadJson(fileName = "name",extension=".json")[0]
        self.plotDataInstance.plot(self.positionArray, self.graphDataLength)
        plt.show(block=True)
        while(True):
            pass

    def runRawDriver(self):
        #self.path = fileOperation.saveToFolder(self.positionArray,name = 'movePathSave')
        #self.dobotHome()    #dobot goes to home position
        #self.oculusHomePosition() #oculus homing operation
        while(1):
            if self.grip is True:   #grip is trigerred
                if self.grip is not self.oldGrip:   #grip changed state, reseting relative coordinates
                    self.path = fileOperation.saveToFolder(self.positionArray, name='movePathSave')
                    self.dobotHome()  # dobot goes to home position
                    #self.oculusHomePosition()  # oculus homing operation
                    self.oculusQuestConnectionInstance.resetZero() #sets coordinates system axis angle correctly
                    self.rebaseOculusToDobotCoordinates()   #home actual position, avoid rapid arm moves
                    self.recording = True
                self.coordinateFromOculusToDobotTranslation() #translating coordinates from oculus to dobot system
                self.moveDobotToPreparedPosition()  #move dobot to position
            else:
                self.recording = False

    def runCloserToPosition(self, maxMove = 30):
        #self.path = fileOperation.saveToFolder(self.positionArray,name = 'movePathSave')
        #self.dobotHome()    #dobot goes to home position
        #self.oculusHomePosition() #oculus homing operation
        while(1):
            if self.grip is True:   #grip is trigerred
                if self.grip is not self.oldGrip:   #grip changed state, reseting relative coordinates
                    self.path = fileOperation.saveToFolder(self.positionArray, name='movePathSave')
                    self.dobotHome()  # dobot goes to home position
                    #self.oculusHomePosition()  # oculus homing operation
                    self.oculusQuestConnectionInstance.resetZero() #sets coordinates system axis angle correctly
                    self.rebaseOculusToDobotCoordinates()   #home actual position, avoid rapid arm moves
                    time.sleep(0.15)
                    self.recording = True
                self.coordinateFromOculusToDobotTranslation() #translating coordinates from oculus to dobot system
                self.moveDobotCloserToPreparedPosition(maxMove)  #move dobot closer to position
            else:
                self.recording = False

    def runPolynomialPrediction(self, backPoints = 10,deg = 5):
        #self.path = fileOperation.saveToFolder(self.positionArray,name = 'movePathSave')
        #self.dobotHome()    #dobot goes to home position
        #self.oculusHomePosition() #oculus homing operation
        while(1):
            if self.grip is True:   #grip is trigerred
                if self.grip is not self.oldGrip:   #grip changed state, reseting relative coordinates
                    self.path = fileOperation.saveToFolder(self.positionArray, name='movePathSave')
                    self.dobotHome()  # dobot goes to home position
                    #self.oculusHomePosition()  # oculus homing operation
                    self.oculusQuestConnectionInstance.resetZero() #sets coordinates system axis angle correctly
                    self.rebaseOculusToDobotCoordinates()   #home actual position, avoid rapid arm moves
                    time.sleep(0.15)
                    self.recording = True
                self.coordinateFromOculusToDobotTranslation() #translating coordinates from oculus to dobot system
                if(len(self.positionArray['timestamp'])>0):
                    self.doPolynomialPrediction(backPoints, deg)
                self.moveDobotToPreparedPosition()  #move dobot to position
            else:
                self.recording = False

    def doPolynomialPrediction(self,backPoints,deg=5,backPointsTime=5,degTime=4):
        #filling with zeros
        pastPointsList = [[],[],[],[]]
        pointIterating = []
        actualTime = time.time()
        for i in range(backPoints):
            pointIterating.append(i)
            pastPointsList[0].append(259.1198)
            pastPointsList[1].append(0)
            pastPointsList[2].append(-8.5687)
            pastPointsList[3].append(actualTime - i*0.3)

        if len(self.positionArray['timestamp']) < backPointsTime:
            backPointsTime = len(self.positionArray['timestamp'])

        #filling with points from array
        for i in range(backPoints):
            pastPointsList[0][-i-1] = self.positionArray['oculusX'][-i-1]
            pastPointsList[1][-i-1] = self.positionArray['oculusY'][-i-1]
            pastPointsList[2][-i-1] = self.positionArray['oculusZ'][-i-1]
            pastPointsList[3][-i-1] = self.positionArray['oculusTimeStamp'][-i-1]
        nextTime = self.polynomialPredictionInstance.predict(pointIterating,pastPointsList[3],degTime,backPointsTime+1)
        #nextTime = actualTime+2
        nextX = self.polynomialPredictionInstance.predict(pastPointsList[3],pastPointsList[0],deg,nextTime)
        nextY = self.polynomialPredictionInstance.predict(pastPointsList[3],pastPointsList[1],deg,nextTime)
        nextZ = self.polynomialPredictionInstance.predict(pastPointsList[3],pastPointsList[2],deg,nextTime)


        # nextX = self.polynomialPredictionInstance.predict(pointIterating,pastPointsList[0],deg,backPoints+1)
        # nextY = self.polynomialPredictionInstance.predict(pointIterating,pastPointsList[1],deg,backPoints+1)
        # nextZ = self.polynomialPredictionInstance.predict(pointIterating,pastPointsList[2],deg,backPoints+1)

        self.dobotX = nextX
        self.dobotY = nextY
        self.dobotZ = nextZ


    #print("X: %0.3f " % xDobot, "Y: %0.3f " % yDobot, "Z: %0.3f " % zDobot)

    #print(position)

    # x = position[0][0] - homePosition[0][0]
    # y = position[0][1] - homePosition[0][1]
    # z = position[0][2] - homePosition[0][2]
    # a = position[0][3] - homePosition[0][3]
    #
    # x1 = position[1][0] - homePosition[1][0]
    # y1 = position[1][1] - homePosition[1][1]
    # z1 = position[1][2] - homePosition[1][2]
    # a1 = position[1][3] - homePosition[1][3]
    #
    # x2 = position[2][0] - homePosition[2][0]
    # y2 = position[2][1] - homePosition[2][1]
    # z2 = position[2][2] - homePosition[2][2]
    # a2 = position[2][3] - homePosition[2][3]
    # print("X: %0.3f " % x,"Y: %0.3f " % y,"Z: %0.3f " % z,"A: %0.3f " % a, "X: %0.3f " % x1,"Y: %0.3f " % y1,"Z: %0.3f " % z1,"A: %0.3f " % a1 , "X: %0.3f " % x2,"Y: %0.3f " % y2,"Z: %0.3f " % z2,"A: %0.3f " % a2)

    # #print(x,y,z)
    #dobotHandlerInstance.setPosition(x,y,z)