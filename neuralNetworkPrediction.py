import tensorflow as tf
import keras

from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
from numpy import array
import rl

class neuralNetworkPrediction:
    def __init__(self):
        self.loud = False
        physical_devices = tf.config.experimental.list_physical_devices('GPU')
        print("physical_devices-------------", len(physical_devices))
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

    def predict(self, dataX=[1, 2, 3], dataY=[1, 4, 9], pastPointsNumber = 2):
        # generate 2d classification dataset
        X, y = make_blobs(n_samples=100, centers=2, n_features=2, random_state=1)
        scalar = MinMaxScaler()
        scalar.fit(X)
        X = scalar.transform(X)
        # define and fit the final model
        model = Sequential()
        model.add(Dense(4, input_dim=2, activation='relu'))
        model.add(Dense(4, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam')
        model.fit(X, y, epochs=500, verbose=0)
        # new instance where we do not know the answer
        Xnew = array([[0.89337759, 0.65864154]])
        # make a prediction
        ynew = model.predict_classes(Xnew)
        # shkeras_scratch_graphow the inputs and predicted outputs
        print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))

class DQN:
    def __init__(self, env):
        self.env = env
        self.memory = deque(maxlen=2000)

        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.01


def create_model(self):
    model = Sequential()
    state_shape = self.env.observation_space.shape
    model.add(Dense(24, input_dim=state_shape[0],
                    activation="relu"))
    model.add(Dense(48, activation="relu"))
    model.add(Dense(24, activation="relu"))
    model.add(Dense(self.env.action_space.n))
    model.compile(loss="mean_squared_error",
                  optimizer=Adam(lr=self.learning_rate))
    return model

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i]
        self.target_model.set_weights(target_weights)

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.model.predict(state)[0])