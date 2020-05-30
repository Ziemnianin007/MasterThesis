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

coordinateOperationInstance = coordinateOperation.coordinateOperation(plot = True, save = True, emulateOculus = False)

coordinateOperationInstance.loadData(plot =False, loop = False)
#coordinateOperationInstance.loadData(path= "C:/Users/jakub/Documents/W4/MasterThesis/PythonProgram/tmp/notWork/movePathSave_date_2020-5-24_19-11-5", plot =False, loop = False)
#coordinateOperationInstance.runRawDriver()
#coordinateOperationInstance.runCloserToPosition(30)
#coordinateOperationInstance.runPolynomialPrediction(backPoints=10,deg=5)
exit()

neuralNetworkPredictionInstance = neuralNetworkPrediction.DQN("Dobot", emulateOculus = False)
#neuralNetworkPredictionInstance = neuralNetworkPrediction.DQN("CartPole-v1")
neuralNetworkPredictionInstance.load()
#neuralNetworkPredictionInstance.fit(True)
neuralNetworkPredictionInstance.fit(False)
#neuralNetworkPredictionInstance.test(15)



#tensorboard --logdir .\logs\CartPoleV1

#tensorboard --logdir .\logs\Dobot







