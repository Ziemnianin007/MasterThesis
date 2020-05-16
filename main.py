import tensorflow as tf
import gym
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

from collections import deque

#import coordinateOperation


#coordinateOperationInstance = coordinateOperation.coordinateOperation(plot = False, save = False)

#coordinateOperationInstance.neuralNetworkPredictionInstance.predict()
#coordinateOperationInstance.loadDataWithLearning() #loading data ============================

#coordinateOperationInstance.runRawDriver()
#coordinateOperationInstance.runCloserToPosition(30)
#coordinateOperationInstance.runPolynomialPrediction(backPoints=10,deg=5)


class DQN:
    def __init__(self, env):
        physical_devices = tf.config.experimental.list_physical_devices('GPU')
        print("physical_devices-------------", len(physical_devices))
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
        self.env = env
        self.memory = deque(maxlen=2000)

        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125

        self.model = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model = Sequential()
        state_shape = self.env.observation_space.shape
        model.add(Dense(24, input_dim=state_shape[0], activation="relu"))
        model.add(Dense(48, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(self.env.action_space.n))
        model.compile(loss="mean_squared_error",
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.model.predict(state)[0])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)


def main():
    env = gym.make("MountainCar-v0")
    gamma = 0.9
    epsilon = .95

    trials = 1000
    trial_len = 500

    # updateTargetNetwork = 1000
    dqn_agent = DQN(env=env)
    steps = []


    for trial in range(trials):
        cur_state = env.reset().reshape(1, 2)
        for step in range(trial_len):
            action = dqn_agent.act(cur_state)
            new_state, reward, done, _ = env.step(action)

            # reward = reward if not done else -20
            new_state = new_state.reshape(1, 2)
            dqn_agent.remember(cur_state, action, reward, new_state, done)

            dqn_agent.replay()  # internally iterates default (prediction) model
            dqn_agent.target_train()  # iterates target model

            cur_state = new_state
            if done:
                break
        if step >= 199:
            print("Failed to complete in trial {}".format(trial))
            if step % 10 == 0:
                dqn_agent.save_model("trial-{}.model".format(trial))
        else:
            print("Completed in {} trials".format(trial))
            dqn_agent.save_model("success.model")
            break

def mainLoad():
    env = gym.make("MountainCar-v0")
    gamma = 0.9
    epsilon = .95

    trials = 1000
    trial_len = 500

    # updateTargetNetwork = 1000
    dqn_agent = DQN(env=env)
    steps = []

    dqn_agent.model.load_weights("success.model")

    cur_state = env.reset().reshape(1, 2)
    action = dqn_agent.act(cur_state)
    new_state, reward, done, _ = env.step(action)

    # reward = reward if not done else -20
    new_state = new_state.reshape(1, 2)
    dqn_agent.remember(cur_state, action, reward, new_state, done)

    dqn_agent.replay()  # internally iterates default (prediction) model
    dqn_agent.target_train()  # iterates target model


    from rl.agents import SARSAAgent
    from rl.policy import EpsGreedyQPolicy
    policy = EpsGreedyQPolicy()



    sarsa = SARSAAgent(model=dqn_agent.model, policy=policy, nb_actions=env.action_space.n)
    sarsa.compile('adam')
    scores = sarsa.test(env, nb_episodes=5, visualize=True)
    return 0

    for trial in range(trials):
        cur_state = env.reset().reshape(1, 2)
        for step in range(trial_len):
            action = dqn_agent.act(cur_state)
            new_state, reward, done, _ = env.step(action)

            # reward = reward if not done else -20
            new_state = new_state.reshape(1, 2)
            dqn_agent.remember(cur_state, action, reward, new_state, done)

            dqn_agent.replay()  # internally iterates default (prediction) model
            dqn_agent.target_train()  # iterates target model

            cur_state = new_state
            if done:
                break
        print("trial {}".format(trial))



#if __name__ == "__main__":
    #mainLoad()


import gym
import random
import numpy as np
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.optimizers import Adam

physical_devices = tf.config.experimental.list_physical_devices('GPU')
print("physical_devices-------------", len(physical_devices))
tf.config.experimental.set_memory_growth(physical_devices[0], True)

env = gym.make('CartPole-v1')

states = env.observation_space.shape[0]
print('States', states)

actions = env.action_space.n
print('Actions', actions)

episodes = 10
for episode in range(1,episodes+1):
    # At each begining reset the game
    state = env.reset()
    # set done to False
    done = False
    # set score to 0
    score = 0
    # while the game is not finished
    while not done:
        # visualize each step
        env.render()
        # choose a random action
        action = random.choice([0,1])
        # execute the action
        n_state, reward, done, info = env.step(action)
        # keep track of rewards
        score+=reward
    print('episode {} score {}'.format(episode, score))


def agent(states, actions):
    model = Sequential()
    model.add(Flatten(input_shape=(1, states)))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    return model


model = agent(env.observation_space.shape[0], env.action_space.n)

from rl.agents import SARSAAgent
from rl.policy import EpsGreedyQPolicy
policy = EpsGreedyQPolicy()

#TODO create env for dobot



sarsa = SARSAAgent(model = model, policy = policy, nb_actions = env.action_space.n)

sarsa.compile('adam', metrics = ['mse'])
sarsa.load_weights('sarsa_weights.h5f')
_ = sarsa.test(env, nb_episodes = 10, visualize= True)
exit()
sarsa.fit(env, nb_steps = 50000, visualize = False, verbose = 1)

scores = sarsa.test(env, nb_episodes = 100, visualize= False)
print('Average score over 100 test games:{}'.format(np.mean(scores.history['episode_reward'])))

sarsa.save_weights('sarsa_weights.h5f', overwrite=True)

# sarsa.load_weights('sarsa_weights.h5f')

_ = sarsa.test(env, nb_episodes = 2, visualize= True)


#https://medium.com/@abhishek.bn93/using-keras-reinforcement-learning-api-with-openai-gym-6c2a35036c83








