import coordinateOperation

coordinateOperationInstance = coordinateOperation.coordinateOperation(plot = True, save = True)

#coordinateOperationInstance.loadData() #loading data ============================

coordinateOperationInstance.runRawDriver()
#coordinateOperationInstance.runCloserToPosition(30)
#coordinateOperationInstance.runPolynomialPrediction(backPoints=10,deg=5)


