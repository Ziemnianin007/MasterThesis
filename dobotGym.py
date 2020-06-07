
import math
import gym
from gym import spaces
import numpy as np
import coordinateOperation
import fileOperation
import threading
import os

class dobotGym(gym.Env):
    def __init__(self, plot = False, save= True, emulateOculus = True, episodeLength = 15, visualize = True, teachingFilesPath = None, dobotDisconnected = False, dobotEmulation = False):
        self.dobotEmulation = dobotEmulation
        self.emulateOculus = emulateOculus
        self.teachingFilesPath = teachingFilesPath
        self.coordinateOperationInstance = coordinateOperation.coordinateOperation(plot = plot, save = save,emulateOculus = self.emulateOculus, dobotDisconnected = dobotDisconnected, dobotEmulation = self.dobotEmulation)
        self.coordinateOperationInstance.recording = False
        # Angle at which to fail the episode

        # Angle limit set to 2 * theta_threshold_radians so failing observation
        # is still within bounds.
        maxStep = 150
        #self.action_space = spaces.Box(low=np.array([-maxStep, -maxStep, -maxStep]), high=np.array([maxStep, maxStep, maxStep]),dtype=np.float32)

        self.minX,self.minY,self.minZ,self.minR = self.coordinateOperationInstance.minX,self.coordinateOperationInstance.minY,self.coordinateOperationInstance.minZ,self.coordinateOperationInstance.minR

        self.maxX,self.maxY,self.maxZ,self.maxR = self.coordinateOperationInstance.maxX,self.coordinateOperationInstance.maxY,self.coordinateOperationInstance.maxZ,self.coordinateOperationInstance.maxR


        self.agentStepsNumberMax = 100
        self.agentStepsNumberActual = 0
        self.agentPositionX = self.coordinateOperationInstance.dobotStartX
        self.agentPositionY = self.coordinateOperationInstance.dobotStartY
        self.agentPositionZ = self.coordinateOperationInstance.dobotStartZ
        self.agentStep = 3

        self.action_space = spaces.Box(np.array([0,0,0,0,0,0]),
                                         np.array([6,6,6,6,6,6]))
        self.observation_space = spaces.Box(np.array([self.minX,self.minY,self.minZ,self.minX,self.minY,self.minZ,self.minX,self.minY,self.minZ, 0]),
                                       np.array([self.maxX,self.maxY,self.maxZ,self.maxX,self.maxY,self.maxZ,self.maxX,self.maxY,self.maxZ, self.agentStepsNumberMax])
                                            ,dtype=np.float32)
        self.visualize = visualize
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

        if(dobotEmulation is True):
            episodeLength = episodeLength * 100

        self.episodeLength = episodeLength -2
        self.episodeStep = 0


        self.teachingFilesList = os.listdir(self.teachingFilesPath)
        self.teachingFilesListIndex = 0
        self.diffSmallRewardOld = 1
        self.diffSmallReward = 0
        self.moveDobot = False
        self.threadDobot = threading.Thread(target=self.moveDobotThreadFunction, name='Thread-b')

        self.threadDobot.start()

    def moveDobotThreadFunction(self):
        while True:
            if(self.moveDobot is True):
                self.coordinateOperationInstance.moveDobotToPreparedPosition()
                self.moveDobot = False

    def refreshState(self):
        if self.dobotEmulation is True:
            self.coordinateOperationInstance.refreshActualPosition()
        np.set_printoptions(precision=3)
        # TODO change positionArray['dobotX'][-1] last dobot
        if(len(self.coordinateOperationInstance.positionArray['dobotZ'])>0):
            self.state = np.array(
                [self.coordinateOperationInstance.positionArray['dobotX'][-1],
                 self.coordinateOperationInstance.positionArray['dobotY'][-1],
                 self.coordinateOperationInstance.positionArray['dobotZ'][-1], self.coordinateOperationInstance.oculusX,
                 self.coordinateOperationInstance.oculusY, self.coordinateOperationInstance.oculusZ,
                 self.agentPositionX, self.agentPositionY, self.agentPositionZ, self.agentStepsNumberActual])
        else:
            self.state = np.array(
                [self.coordinateOperationInstance.rightXLastDobot, self.coordinateOperationInstance.rightYLastDobot,
                 self.coordinateOperationInstance.rightZLastDobot, self.coordinateOperationInstance.oculusX,
                 self.coordinateOperationInstance.oculusY, self.coordinateOperationInstance.oculusZ,
                 self.agentPositionX, self.agentPositionY, self.agentPositionZ, self.agentStepsNumberActual])



    def moveAgent(self,action):
        #self.agentStep = self.agentStepsNumberMax - self.agentStepsNumberActual

        if action == 0:
            self.agentPositionX += self.agentStep
        elif action == 1:
            self.agentPositionX += -self.agentStep
        elif action == 2:
            self.agentPositionY += self.agentStep
        elif action == 3:
            self.agentPositionY += -self.agentStep
        elif action == 4:
            self.agentPositionZ += self.agentStep
        elif action == 5:
            self.agentPositionZ += -self.agentStep

        tooFar = False
        if  self.agentPositionX < self.minX:
            self.agentPositionX = self.minX
            tooFar = True
        if  self.agentPositionX > self.maxX:
            self.agentPositionX = self.maxX
            tooFar = True

        if  self.agentPositionY < self.minY:
            self.agentPositionY = self.minY
            tooFar = True
        if  self.agentPositionY > self.maxY:
            self.agentPositionY = self.maxY
            tooFar = True

        if  self.agentPositionZ < self.minZ:
            self.agentPositionZ = self.minZ
            tooFar = True
        if  self.agentPositionZ > self.maxZ:
            self.agentPositionZ = self.maxZ
            tooFar = True

        R = math.sqrt(self.agentPositionX**2+self.agentPositionY**2)
        if self.agentPositionY == 0:
            self.agentPositionY = 0.001
        tg = self.agentPositionX/self.agentPositionY
        if R == 0:
            R = 0.001
        if(R<self.minR):
            self.agentPositionX = self.agentPositionX * self.minR / R
            self.agentPositionY = self.agentPositionY * self.minR / R
            tooFar = True
        if(R>self.maxR):
            self.agentPositionX = self.agentPositionX * self.maxR / R
            self.agentPositionY = self.agentPositionY * self.maxR / R
            tooFar = True


        if tooFar is True:
            self.diffSmallReward = self.diffSmallReward/10

    def step(self, action):
        info = {
            'Diff': self.coordinateOperationInstance.actualDiffXYZ,
        }
        self.diffSmallReward = 1/(math.sqrt((self.state[3]-self.state[6])** 2+(self.state[4]-self.state[7])** 2+(self.state[5]-self.state[8])** 2)/25+0.5)
        if (self.diffSmallReward > self.diffSmallRewardOld):
            self.diffSmallRewardOld = self.diffSmallReward
            self.diffSmallReward += 1
            #self.diffSmallReward +=1
        else:
            self.diffSmallRewardOld = self.diffSmallReward

        self.moveAgent(action)
        self.agentStepsNumberActual += 1
        self.refreshState()
        done = False
        if(self.agentStepsNumberActual < self.agentStepsNumberMax and self.moveDobot):
            return np.array(self.state), self.diffSmallReward, done, info
        else:
            self.agentStepsNumberActual = 0
        digit = '%.1f'
        np.set_printoptions(precision=3)
        print("\nAction: ", action, " Step: ",self.agentStepsNumberMax,"/", self.agentStepsNumberActual, " LDX: ", digit % self.state[0], "LDY: ", digit % self.state[1], " LDZ: ", digit % self.state[2],
              " OcX: ",digit % self.state[3], " OcY: ",digit % self.state[4], " OcZ: ",digit % self.state[5], " AgX: ",self.state[6], " AgY: ",self.state[7], " AgZ: ",self.state[8], " S:",self.state[9])
        self.coordinateOperationInstance.coordinateFromOculusToDobotTranslation() #translating coordinates from oculus to dobot system
        self.coordinateOperationInstance.setDobotPositionToMove(self.agentPositionX,self.agentPositionY,self.agentPositionZ)

        self.moveDobot = True

        reward = 1/(self.coordinateOperationInstance.actualDiffXYZ/25+1)*self.agentStepsNumberMax*8
        if self.coordinateOperationInstance.grip is True:
            done = False
        else:
            done = True

        if (self.episodeStep > self.episodeLength):
            done = True

        self.episodeStep += 1
        self.refreshState()
        return np.array(self.state), reward, done, info

    def reset(self):
        while(self.moveDobot is True):
            pass
        self.coordinateOperationInstance.endOfMoving()
        if self.visualize:
            self.coordinateOperationInstance.plotNow()

        self.coordinateOperationInstance.preparationForMoving()
        while(self.coordinateOperationInstance.grip is False and self.emulateOculus is not True):
            pass
        self.episodeStep = 0

        if(self.emulateOculus):
            self.loadOculusDataFromFolder()

        self.coordinateOperationInstance.preparationForMoving()
        self.agentStepsNumberActual = 0
        self.agentPositionX = self.coordinateOperationInstance.dobotStartX
        self.agentPositionY = self.coordinateOperationInstance.dobotStartY
        self.agentPositionZ = self.coordinateOperationInstance.dobotStartZ
        self.refreshState()
        self.diffSmallRewardOld = 1
        self.coordinateOperationInstance.startRecording()
        return np.array(self.state)

    def loadOculusDataFromFolder(self):
        if len(self.teachingFilesList) <= self.teachingFilesListIndex:
            self.teachingFilesListIndex = 0
        path = self.teachingFilesPath + "\\" + self.teachingFilesList[self.teachingFilesListIndex].split(".")[0]
        print("Loading VR path file number: ", self.teachingFilesListIndex, " from: ", path)

        self.coordinateOperationInstance.oculusQuestEmulationLoadData(self.coordinateOperationInstance.loadData(path = path,plot =False , loop = False))
        self.teachingFilesListIndex += 1

    def close(self):
        self.coordinateOperationInstance.endOfMoving()