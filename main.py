import tensorflow as tf
import gym
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

from collections import deque

import coordinateOperation

import neuralNetworkPrediction

#coordinateOperationInstance = coordinateOperation.coordinateOperation(plot = True, save = True)

#coordinateOperationInstance.runRawDriver()
#coordinateOperationInstance.runCloserToPosition(30)
#coordinateOperationInstance.runPolynomialPrediction(backPoints=10,deg=5)

#neuralNetworkPredictionInstance = neuralNetworkPrediction.DQN("Dobot")
neuralNetworkPredictionInstance = neuralNetworkPrediction.DQN("Dobot")
#neuralNetworkPredictionInstance.load()
#neuralNetworkPredictionInstance.fit(True)
neuralNetworkPredictionInstance.fit(False)
#neuralNetworkPredictionInstance.test(15)



#tensorboard --logdir .\logs\CartPoleV1

#tensorboard --logdir .\logs\Dobot







