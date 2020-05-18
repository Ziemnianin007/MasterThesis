import tensorflow as tf
import keras
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
from numpy import array
from collections import deque


import gym
import random
import numpy as np
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.optimizers import Adam

from keras.layers import LSTM
from rl.agents import SARSAAgent
from rl.policy import EpsGreedyQPolicy

class DQN:
    def __init__(self):

        physical_devices = tf.config.experimental.list_physical_devices('GPU')
        print("physical_devices-------------", len(physical_devices))
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

        self.env = gym.make('CartPole-v1')

        states = self.env.observation_space.shape[0] #To get an idea about the number of variables affecting the environment
        print('States', states)

        actions = self.env.action_space.n # To get an idea about the number of possible actions in the environment, do [right,left]
        print('Actions', actions)

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

        self.model = self.agent(self.env.observation_space.shape[0], self.env.action_space.n)

        self.policy = EpsGreedyQPolicy()
        # TODO create env for dobot

        self.sarsa = SARSAAgent(model=self.model, policy=self.policy, nb_actions=self.env.action_space.n)

    def agent(self, states, actions):
        n_steps_in = 5
        n_features = 24
        self.model = Sequential()
        #model.add(Flatten(input_shape=(1, states)))
        self.model.add(LSTM(4, activation='relu',input_shape=(1, 4))) #, stateful=False states are resetted together after each batch.
        self.model.add(Dense(24, activation='relu'))
        self.model.add(Dense(24, activation='relu'))
        self.model.add(Dense(24, activation='relu'))
        self.model.add(Dense(actions, activation='linear'))
        #model.reset_states()
        return self.model

    def load(self):
        self.sarsa.compile('adam', metrics=['mse'])
        self.sarsa.load_weights('sarsa_weights.h5f')
        self.sarsa.compile('adam', metrics=['mse'])

    def test(self,nb_episodes=2):
        _ = self.sarsa.test(self.env, nb_episodes = nb_episodes, visualize=True)

    def fit(self,visualize = False):
        self.sarsa.compile('adam', metrics=['mse'])
        self.sarsa.fit(self.env, nb_steps=50000, visualize=visualize, verbose=1, nb_max_start_steps  = 1, start_step_policy = self.model.reset_states)

        scores = self.sarsa.test(self.env, nb_episodes=100, visualize=visualize)
        print('Average score over 100 test games:{}'.format(np.mean(scores.history['episode_reward'])))

        self.sarsa.save_weights('sarsa_weights.h5f', overwrite=True)

    # https://medium.com/@abhishek.bn93/using-keras-reinforcement-learning-api-with-openai-gym-6c2a35036c83