import keras

from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
from numpy import array

class neuralNetworkPrediction:
    def __init__(self):
        self.loud = False

    def predict(self, dataX=[1, 2, 3], dataY=[1, 4, 9], pastPointsNumber):
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
        # show the inputs and predicted outputs
        print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))
