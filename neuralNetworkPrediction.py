
import os
import tensorflow as tf
import keras
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
from numpy import array
from collections import deque

import fileOperation
import gym
import random
import numpy as np
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.optimizers import Adam
import rl
from keras.layers import LSTM
from rl.agents import SARSAAgent
from rl.policy import EpsGreedyQPolicy
import dobotGym
from datetime import datetime
from livelossplot import PlotLossesKeras

class DQN:
    def __init__(self, env = "CartPole-v1"):

        os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
        physical_devices = tf.config.experimental.list_physical_devices('GPU')
        print("physical_devices-------------", len(physical_devices))
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

        if env == "CartPole-v1":
            self.env = gym.make('CartPole-v1')
            self.states = self.env.observation_space.shape[0]
            self.actions = self.env.action_space.n
            self.saveFileName = 'sarsa_weights.h5f'
            logdir = "logs/CartPoleV1/" + datetime.now().strftime("%Y%m%d-%H%M%S")
            self.tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)
            self.visualize = True
        elif env == "Dobot":
            self.env = dobotGym.dobotGym()
            self.states = self.env.observation_space.shape[0]
            self.actions = self.env.action_space.shape[0]
            self.saveFileName = 'sarsa_weights_dobot.h5f'
            logdir = "logs/Dobot/" + datetime.now().strftime("%Y%m%d-%H%M%S")
            self.tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)
            self.visualize = True
        else:
            raise TypeError("Wrong env")

        print('States', self.states)#To get an idea about the number of variables affecting the environment
        print('Actions', self.actions) # To get an idea about the number of possible actions in the environment, do [right,left]


        #

        # episodes = 10
        # for episode in range(1, episodes + 1):
        #     # At each begining reset the game
        #     state = self.env.reset()
        #     # set done to False
        #     done = False
        #     # set score to 0
        #     score = 0
        #     # while the game is not finished
        #     while not done:
        #         # visualize each step
        #         self.env.render()
        #         # choose a random action
        #         action = random.choice([0, 1])
        #         # execute the action
        #         n_state, reward, done, info = self.env.step(action)
        #         # keep track of rewards
        #         score += reward
        #     print('episode {} score {}'.format(episode, score))

        self.model = self.agentSarsa(self.states, self.actions)

        self.policy = EpsGreedyQPolicy()
        # TODO agent type: DDPGAgent in continues mode

        self.agent = SARSAAgent(model=self.model, policy=self.policy, nb_actions=self.actions)
        self.agent._is_graph_network = True
        def t():
            return False
        self.agent._in_multi_worker_mode = t

        self.agent.save = self.saveAgentWeights
    def saveAgentWeights(self,path, overwrite=True):
        path = 'model/checkpoint/' + datetime.now().strftime("%Y%m%d-%H%M%S") + self.saveFileName
        self.agent.save_weights(path,overwrite)
    def agentSarsa(self, states, actions):
        n_steps_in = 5
        n_features = 24
        self.model = Sequential()
        #model.add(Flatten(input_shape=(1, states)))
        self.model.add(LSTM(4, activation='relu',input_shape=(1, states))) #, stateful=False states are resetted together after each batch.
        self.model.add(Dense(24, activation='relu'))
        self.model.add(Dense(24, activation='relu'))
        self.model.add(Dense(24, activation='relu'))
        self.model.add(Dense(actions, activation='linear'))
        #dot_img_file = '/model_1.png'
        #keras.utils.plot_model(self.model, to_file=dot_img_file, show_shapes=True)
        #model.reset_states()
        return self.model

    def load(self):
        path = fileOperation.openDialogFunction(".h5f")
        self.agent.compile('adam', metrics=['mse'])
        self.agent.load_weights(path)
        self.agent.compile('adam', metrics=['mse'])

    def test(self,nb_episodes=2):
        _ = self.agent.test(self.env, nb_episodes = nb_episodes, visualize=self.visualize)

    def fit(self,visualize = False):
        checkpoint_filepath = 'model/checkpoint/'
        model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_filepath,
            save_weights_only=False,
            save_freq=25
        )
        self.agent.compile('adam', metrics=['mse'])
        self.agent.fit(self.env, nb_steps=50000, log_interval=25,  visualize=visualize, verbose=1, nb_max_start_steps  = 1, start_step_policy = self.model.reset_states,

                       #callbacks=[PlotLossesKeras()])
    callbacks=[self.tensorboard_callback,model_checkpoint_callback],)

        scores = self.agent.test(self.env, nb_episodes=100, visualize=visualize)
        print('Average score over 100 test games:{}'.format(np.mean(scores.history['episode_reward'])))

        self.agent.save_weights(self.saveFileName, overwrite=True)


    # https://medium.com/@abhishek.bn93/using-keras-reinforcement-learning-api-with-openai-gym-6c2a35036c83