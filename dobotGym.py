
import math
import gym
from gym import spaces
import numpy as np
import coordinateOperation
import fileOperation

class dobotGym(gym.Env):
    def __init__(self, plot = False, save= True):
        self.coordinateOperationInstance = coordinateOperation.coordinateOperation(plot, save)
        self.coordinateOperationInstance.recording = False

        # Angle at which to fail the episode

        # Angle limit set to 2 * theta_threshold_radians so failing observation
        # is still within bounds.
        maxStep = 150
        #self.action_space = spaces.Box(low=np.array([-maxStep, -maxStep, -maxStep]), high=np.array([maxStep, maxStep, maxStep]),dtype=np.float32)

        self.action_space = spaces.Box(np.array([self.coordinateOperationInstance.minX,self.coordinateOperationInstance.minY,self.coordinateOperationInstance.minZ]),
                                       np.array([self.coordinateOperationInstance.maxX,self.coordinateOperationInstance.maxY,self.coordinateOperationInstance.maxZ])
                                            ,dtype=np.float32)

        self.observation_space = spaces.Box(np.array([self.coordinateOperationInstance.minX,self.coordinateOperationInstance.minY,self.coordinateOperationInstance.minZ]),
                                       np.array([self.coordinateOperationInstance.maxX,self.coordinateOperationInstance.maxY,self.coordinateOperationInstance.maxZ])
                                            ,dtype=np.float32)

        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def step(self, action):
        print("Action", action, self.action_space.low, self.action_space.high)
        action = np.clip(action, self.action_space.low, self.action_space.high)
        print(action)
        self.coordinateOperationInstance.coordinateFromOculusToDobotTranslation() #translating coordinates from oculus to dobot system
        self.coordinateOperationInstance.setDiffPositionToMove(action[0],action[1],action[2])
        self.state = self.coordinateOperationInstance.moveDobotToPreparedPosition()

        reward = 1/(self.coordinateOperationInstance.actualDiffXYZ+1)

        if self.coordinateOperationInstance.grip is True:
            done = False
        else:
            done = True

        info = {
            'Diff': self.coordinateOperationInstance.actualDiffXYZ,
        }

        return np.array(self.state), reward, done, info

    def reset(self):
        self.coordinateOperationInstance.preparationForMoving()
        self.state = np.array([self.coordinateOperationInstance.rightXLastDobot,self.coordinateOperationInstance.rightYLastDobot,self.coordinateOperationInstance.rightZLastDobot])
        while(self.coordinateOperationInstance.grip is False):
            pass
        return np.array(self.state)


    def close(self):
        self.coordinateOperationInstance.endOfMoving()