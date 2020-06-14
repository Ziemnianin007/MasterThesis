import os
from math import dist

class analysis:
    def __init__(self, teachingFilesPath):
        self.teachingFilesPath = teachingFilesPath
        self.teachingFilesListIndex = 0
        self.teachingFilesList = os.listdir(self.teachingFilesPath)

    def loadOculusDataFromFolder(self):
        if len(self.teachingFilesList) <= self.teachingFilesListIndex:
            self.teachingFilesListIndex = 0
        path = self.teachingFilesPath + "\\" + self.teachingFilesList[self.teachingFilesListIndex].split(".")[0]
        print("Loading VR path file number: ", self.teachingFilesListIndex, " from: ", path)

        loadedData = self.loadData(path=path, plot=False, loop=False)
        self.teachingFilesListIndex += 1
        return loadedData

    def calculateDistance(self,point1, point2):
        pass

    def anlalyseData(self,data):
        dobotPosition = []
        predictionPosition = []
        oculusPosition = []
        dobotPosition.append(data["dobotX"])
        dobotPosition.append(data["dobotY"])
        dobotPosition.append(data["dobotZ"])
        predictionPosition.append(data["predictionX"])
        predictionPosition.append(data["predictionY"])
        predictionPosition.append(data["predictionZ"])
        oculusPosition.append(data["oculusXSynchronized"])
        oculusPosition.append(data["oculusYSynchronized"])
        oculusPosition.append(data["oculusZSynchronized"])
        VR_ARM = dist((dobotPosition[0],dobotPosition[1],dobotPosition[2]), (oculusPosition[0], oculusPosition[1], oculusPosition[2]))
        VR_PRE = dist((predictionPosition[0],predictionPosition[1],predictionPosition[2]), (oculusPosition[0], oculusPosition[1], oculusPosition[2]))
        PRE_ARM = dist((dobotPosition[0],dobotPosition[1],dobotPosition[2]), (predictionPosition[0], predictionPosition[1], predictionPosition[2]))
        print("VR_ARM: ", VR_ARM, " VR_PRE ", VR_PRE, "PRE_ARM", PRE_ARM)







