import dobotHandler
import oculusQuestConnection
import pprint
import plotData

class coordinateOperation:
    def __init__(self, graphDataLength = 50):
        #home dobot magician in dobotstudio, then disconnect and run
        self.dobotHandlerInstance = dobotHandler.dobotHandler()
        self.oculusQuestConnectionInstance = oculusQuestConnection.oculusQuestConnection()
        self.oculusHomePosition()
        self.grip = False
        self.getActualPosition()
        self.positionArray = []
        self.dobotPositionTimeStamp = None
        self.plotDataInstance = plotData.plotData()
        self.graphDataLength = graphDataLength

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

    def oculusHomePosition(self):
        homePosition = self.oculusQuestConnectionInstance.getPosition()
        self.homeX = homePosition[0][3]
        self.homeY = homePosition[2][3]
        self.homeZ = homePosition[1][3]
        return(self.homeX,self.homeY,self.homeZ)

    def getActualPosition(self):
        position = self.oculusQuestConnectionInstance.getPosition()
        self.oldGrip = self.grip
        self.grip = self.oculusQuestConnectionInstance.getRightControllerGrip()
        self.rightX = position[0][3] - self.homeX  # +- 0.25
        self.rightY = position[2][3] - self.homeY  # += 0.25
        self.rightZ = position[1][3] - self.homeZ  # +0.5 -0.1
        print("X: %0.3f " % self.rightX, "Y: %0.3f " % self.rightY, "Z: %0.3f " % self.rightZ, " grip: ", self.grip)
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

        self.positionArray['timestamp'] = []

    def coordinateFromOculusToDobotTranslation(self):

        #self.dobotX = -self.rightY / 0.25 * 231.5 + 259.1198
        #self.dobotY = -self.rightX / 0.25 * 328 + 0
        #self.dobotZ = self.rightZ / 0.25 * 150 + 0 - 8.5687
        self.dobotX = -self.rightY *1000 + 259.1198
        self.dobotY = -self.rightX *1000 + 0
        self.dobotZ = self.rightZ *1000 + 0 - 8.5687
        if self.dobotZ < -30:    #avoid ground contact
            self.dobotZ = -30
        self.rightXLastDobot = self.rightX
        self.rightYLastDobot = self.rightY
        self.rightZLastDobot = self.rightZ

    def rebaseOculusToDobotCoordinates(self):
        self.homeX = self.homeX + (self.rightX - self.rightXLastDobot)
        self.homeY = self.homeY + (self.rightY - self.rightYLastDobot)
        self.homeZ = self.homeZ + (self.rightZ - self.rightZLastDobot)

    def moveDobotToPreparedPosition(self):
        self.dobotPositionTimeStamp = self.dobotHandlerInstance.setPosition(self.dobotX, self.dobotY, self.dobotZ)
        self.postionArrayAddDobotAndOculusPositions()

    def moveDobotCloserToPreparedPosition(self,maxMove = 30):
        self.dobotPositionTimeStamp =self.dobotHandlerInstance.closerToPosition(self.dobotX, self.dobotY, self.dobotZ, maxMove)
        self.postionArrayAddDobotAndOculusPositions()

    def postionArrayAddDobotAndOculusPositions(self):
        self.positionArray['oculusX'].append(self.dobotX)
        self.positionArray['oculusY'].append(self.dobotY)
        self.positionArray['oculusZ'].append(self.dobotZ)

        self.positionArray['dobotX'].append(self.dobotPositionTimeStamp[0][0])
        self.positionArray['dobotY'].append(self.dobotPositionTimeStamp[0][1])
        self.positionArray['dobotZ'].append(self.dobotPositionTimeStamp[0][2])

        self.positionArray['timestamp'].append(self.dobotPositionTimeStamp[1])
        self.plotDataInstance.plot(self.positionArray['dobotX'],self.positionArray['timestamp'])
        #pprint.pprint(self.positionArray)

    def runRawDriver(self):
        self.dobotHome()    #dobot goes to home position
        self.oculusHomePosition() #oculus homing operation
        while(1):
            self.getActualPosition()    #getting actual position from oculus
            if self.grip is True:   #grip is trigerred
                if self.grip is not self.oldGrip:   #grip changed state, reseting relative coordinates
                    self.oculusQuestConnectionInstance.resetZero() #sets coordinates system axis angle correctly
                    self.rebaseOculusToDobotCoordinates()   #home actual position, avoid rapid arm moves
                    self.getActualPosition()
                self.coordinateFromOculusToDobotTranslation() #translating coordinates from oculus to dobot system
                self.moveDobotToPreparedPosition()  #move dobot to position

    def runCloserToPosition(self, maxMove = 30):
        self.dobotHome()    #dobot goes to home position
        self.oculusHomePosition() #oculus homing operation
        while(1):
            self.getActualPosition()    #getting actual position from oculus
            if self.grip is True:   #grip is trigerred
                if self.grip is not self.oldGrip:   #grip changed state, reseting relative coordinates
                    self.oculusQuestConnectionInstance.resetZero() #sets coordinates system axis angle correctly
                    self.rebaseOculusToDobotCoordinates()   #home actual position, avoid rapid arm moves
                    self.getActualPosition()
                self.coordinateFromOculusToDobotTranslation() #translating coordinates from oculus to dobot system
                self.moveDobotCloserToPreparedPosition(maxMove)  #move dobot closer to position


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