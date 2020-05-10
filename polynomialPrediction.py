import numpy
class polynomalPrediction():
    def __init__(self):
        self.loud = True

    def predict(self,dataX = [1, 2, 3], dataY = [1, 4, 9], deg= 5, actualIn= 2):

        coeff = numpy.polynomial.polynomial.polyfit(dataX, dataY, deg, full =True)
        if self.loud is True: print("Coeff:", coeff[0])
        if self.loud is True: print("Matching:", coeff[1])

        calculated = numpy.polynomial.polynomial.polyval(actualIn,coeff[0])
        if self.loud is True: print(calculated)
        return calculated
