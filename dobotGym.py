
import math
import gym
from gym import spaces
import numpy as np
import coordinateOperation
import fileOperation

class dobotGym(gym.Env):
    def __init__(self, plot = False, save= True, emulateOculus = True, episodeLength = 15):
        self.coordinateOperationInstance = coordinateOperation.coordinateOperation(plot = plot, save = save,emulateOculus = emulateOculus)
        self.coordinateOperationInstance.recording = False

        # Angle at which to fail the episode

        # Angle limit set to 2 * theta_threshold_radians so failing observation
        # is still within bounds.
        maxStep = 150
        #self.action_space = spaces.Box(low=np.array([-maxStep, -maxStep, -maxStep]), high=np.array([maxStep, maxStep, maxStep]),dtype=np.float32)

        self.minX,self.minY,self.minZ = self.coordinateOperationInstance.minX,self.coordinateOperationInstance.minY,self.coordinateOperationInstance.minZ

        self.maxX,self.maxY,self.maxZ = self.coordinateOperationInstance.maxX,self.coordinateOperationInstance.maxY,self.coordinateOperationInstance.maxZ


        self.agentStepsNumberMax = 20
        self.agentStepsNumberActual = 0
        self.agentPositionX = 0
        self.agentPositionY = 0
        self.agentPositionZ = 0
        self.agentStep = 1

        self.action_space = spaces.Box(np.array([0,0,0,0,0,0]),
                                         np.array([6,6,6,6,6,6]))
        self.observation_space = spaces.Box(np.array([self.minX,self.minY,self.minZ,self.minX,self.minY,self.minZ,self.minX,self.minY,self.minZ, 0]),
                                       np.array([self.maxX,self.maxY,self.maxZ,self.maxX,self.maxY,self.maxZ,self.maxX,self.maxY,self.maxZ, self.agentStepsNumberMax])
                                            ,dtype=np.float32)

        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

        self.episodeLength = episodeLength -2
        self.episodeStep = 0



    def refreshState(self):
        np.set_printoptions(precision=3)
        self.state = np.array(
            [self.coordinateOperationInstance.rightXLastDobot, self.coordinateOperationInstance.rightYLastDobot,
             self.coordinateOperationInstance.rightZLastDobot, self.coordinateOperationInstance.oculusX, self.coordinateOperationInstance.oculusY, self.coordinateOperationInstance.oculusZ,
             self.agentPositionX, self.agentPositionY, self.agentPositionZ, self.agentStepsNumberActual])

    def moveAgent(self,action):
        self.agentStep = self.agentStepsNumberMax - self.agentStepsNumberActual

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

        if  self.agentPositionX < self.minX:
            self.agentPositionX = self.minX
        if  self.agentPositionX > self.maxX:
            self.agentPositionX = self.maxX

        if  self.agentPositionY < self.minY:
            self.agentPositionY = self.minY
        if  self.agentPositionY > self.maxY:
            self.agentPositionY = self.maxY

        if  self.agentPositionZ < self.minZ:
            self.agentPositionZ = self.minZ
        if  self.agentPositionZ > self.maxZ:
            self.agentPositionZ = self.maxZ

    def step(self, action):
        info = {
            'Diff': self.coordinateOperationInstance.actualDiffXYZ,
        }
        diffSmallReward = 1/(math.sqrt((self.state[3]-self.state[6])** 2+(self.state[4]-self.state[7])** 2+(self.state[5]-self.state[8])** 2)+1)

        self.moveAgent(action)
        self.agentStepsNumberActual += 1
        self.refreshState()
        done = False
        if(self.agentStepsNumberActual < self.agentStepsNumberMax):
            return np.array(self.state), diffSmallReward, done, info
        else:
            self.agentStepsNumberActual = 0

        print("Action: ", action, " Step: ",self.agentStepsNumberMax,"/", self.agentStepsNumberActual," State: ", self.state)
        self.coordinateOperationInstance.coordinateFromOculusToDobotTranslation() #translating coordinates from oculus to dobot system
        self.coordinateOperationInstance.setDiffPositionToMove(self.agentPositionX,self.agentPositionY,self.agentPositionZ)
        self.coordinateOperationInstance.moveDobotToPreparedPosition()

        reward = 1/(self.coordinateOperationInstance.actualDiffXYZ+1)*self.agentStepsNumberMax*4
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
        self.coordinateOperationInstance.endOfMoving()
        self.episodeStep = 0
        self.coordinateOperationInstance.preparationForMoving()
        self.refreshState()
        self.agentStepsNumberActual = 0
        while(self.coordinateOperationInstance.grip is False):
            pass
        self.coordinateOperationInstance.startRecording()
        return np.array(self.state)


    def close(self):
        self.coordinateOperationInstance.endOfMoving()