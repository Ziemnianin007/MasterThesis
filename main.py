import tensorflow as tf
import gym
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from rl.policy import EpsGreedyQPolicy

from collections import deque

import coordinateOperation

import neuralNetworkPrediction

#coordinateOperationInstance = coordinateOperation.coordinateOperation(plot = True, save = True, emulateOculus = True,dobotDisconnected=True)

#coordinateOperationInstance.loadData(plot =True , loop = True)
#coordinateOperationInstance.loadData(path= "C:/Users/jakub/Documents/W4/MasterThesis/PythonProgram/tmp/notWork/movePathSave_date_2020-5-24_19-11-5", plot =False, loop = False)
#coordinateOperationInstance.runRawDriver()
#coordinateOperationInstance.runCloserToPosition(30)
#coordinateOperationInstance.runPolynomialPrediction(backPoints=10,deg=5)
#exit()

neuralNetworkPredictionInstance = neuralNetworkPrediction.DQN("Dobot", emulateOculus = True, visualize = True, teachingFilesPath = "C:\\Users\\jakub\\Documents\\W4\\MasterThesis\\PythonProgram\\tmp\\teach",
                                                              policyValues = {"inner_policy": EpsGreedyQPolicy(), "attr":"eps", "value_max":0.8, "value_min":.2, "value_test":.0, "nb_steps":2000000},
                                                              dobotEmulation = True)
#neuralNetworkPredictionInstance = neuralNetworkPrediction.DQN("CartPole-v1")
#neuralNetworkPredictionInstance.load()
#neuralNetworkPredictionInstance.fit(True)
neuralNetworkPredictionInstance.fit(False)
#neuralNetworkPredictionInstance.test(15)



#tensorboard --logdir .\logs\CartPoleV1

#tensorboard --logdir .\logs\Dobot







