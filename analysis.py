import os
import math
import fileOperation
import statistics

class analysis:
    def __init__(self, teachingFilesPath):
        self.teachingFilesPath = teachingFilesPath
        self.teachingFilesListIndex = 0
        self.teachingFilesList = os.listdir(self.teachingFilesPath)

    def repairData(self, positionArray):
        length = []
        for key, list in positionArray.items():
            length.append(len(list))
        minimalLength = min(length)
        if (minimalLength == 0):
            print("Loaded data have length 0")
        reducedArray = {}
        for key, list in positionArray.items():
            reducedArray[key] = list[0:minimalLength - 1]
        longerArray = {}
        longerArray['oculusX'] = positionArray['oculusX']
        longerArray['oculusY'] = positionArray['oculusY']
        longerArray['oculusZ'] = positionArray['oculusZ']
        longerArray['oculusTimeStamp'] = positionArray['oculusTimeStamp']

        length = []
        for key, list in longerArray.items():
            length.append(len(list))
        minimalLength = min(length)
        if (minimalLength == 0):
            print("Loaded data have length 0")
        reducedLongerArray = {}
        for key, list in longerArray.items():
            reducedLongerArray[key] = list[0:minimalLength - 1]

        positionArray = reducedArray
        for key, list in reducedLongerArray.items():
            positionArray[key] = list
        return positionArray

    def loadData(self, plot = False, path = None, loop = False):
        thisPath = path
        positionArray = None
        while(True):
            positionArray, path = fileOperation.loadJson(fileName = "name",extension=".json", thisPath = thisPath)
            positionArray = self.repairData(positionArray)
            if plot is True:
                self.plotDataInstance.plot(positionArray, self.graphDataLength, title = path.split("/")[-1].split(".")[0])
                #plt.show()
            if loop is False:
                break
        return positionArray

    def loadOculusDataFromFolder(self):
        if len(self.teachingFilesList) <= self.teachingFilesListIndex:
            self.teachingFilesListIndex = 0
        path = self.teachingFilesPath + "\\" + self.teachingFilesList[self.teachingFilesListIndex].split(".")[0]
        print("Loading VR path file number: ", self.teachingFilesListIndex, "name: ",self.teachingFilesList[self.teachingFilesListIndex].split(".")[0], " from: ", path)

        loadedData = self.loadData(path=path, plot=False, loop=False)
        filename = self.teachingFilesList[self.teachingFilesListIndex].split(".")[0]
        self.teachingFilesListIndex += 1
        return loadedData , filename

    def analyseAllFiles(self):
        analysed = []
        for file in self.teachingFilesList:
            analysed.append(self.analyseFile())
        for line in analysed:
            print(line)


    def analyseFile(self):
        loadedData, filename = self.loadOculusDataFromFolder()
        VR_ARM, VR_PRE, PRE_ARM =[],[],[]
        for index in range(len(loadedData["oculusZSynchronized"])):

            oneLineDict = {}
            for key,value in loadedData.items():
                oneLineDict[key] = loadedData[key][index]
            analysied = self.anlalyseData(oneLineDict)
            VR_ARM.append(analysied[0])
            VR_PRE.append(analysied[1])
            PRE_ARM.append(analysied[2])
        print()
        print(filename, " ","VR_ARM: ",statistics.mean(VR_ARM),"+-",statistics.stdev(VR_ARM), "       ","VR_PRE: ",statistics.mean(VR_PRE),"+-",statistics.stdev(VR_PRE), " ", "        ","PRE_ARM: ",statistics.mean(PRE_ARM),"+-",statistics.stdev(PRE_ARM), " ")
        print()

        return [filename, " ","VR_ARM: ",statistics.mean(VR_ARM),"+-",statistics.stdev(VR_ARM), " ","VR_PRE: ",statistics.mean(VR_PRE),"+-",statistics.stdev(VR_PRE), " ","PRE_ARM: ",statistics.mean(PRE_ARM),"+-",statistics.stdev(PRE_ARM), " "]



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

        def distance(v1, v2):
            return sum([(x - y) ** 2 for (x, y) in zip(v1, v2)]) ** (0.5)

        VR_ARM = distance(dobotPosition, oculusPosition)
        VR_PRE = distance(predictionPosition,oculusPosition)
        PRE_ARM = distance(dobotPosition, predictionPosition)
        #print("VR_ARM: ", VR_ARM, " VR_PRE ", VR_PRE, "PRE_ARM", PRE_ARM)
        return [VR_ARM,VR_PRE,PRE_ARM]







