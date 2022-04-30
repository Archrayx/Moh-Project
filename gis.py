import numpy as np
import networkx as nx
import pandas as pd
import time


class gis:
    # used to store final output of query
    final_results = []
    # used to hold current query
    currentlySelected = []

    # Options hashmap for selecting query options
    ATR_OPTIONS = {"name": 1, "state": 2, "latitude": 3,
                   "longitude": 4, "population": 5}

    # simple global variables used to hold parsing/file data
    # accessed in class methods later
    dataDict = {}
    file = ""
    data = ""
    dataList = []

    # Ctor
    def __init__(self):
        self.file = open("gis.dat", "r")
        self.data = self.file.read()
        self.dataList = self.data.split("\n")[4:]
        pass

    ###################################################
    #Selets a Set of Cities With Conditional Arguments#
    ###################################################
    def selectCities(self, attribute, lowerBound, upperBound):
        attribute = attribute.lower()
        (isAnAtr, atrValue) = self.isAtrValid(attribute)
        isALowerBound = self.isBoundValid(atrValue, lowerBound)
        isAnUpperBound = self.isBoundValid(atrValue, upperBound)

        if (isAnAtr, isALowerBound, isAnUpperBound):
            pass
        pass

    ######################################
    #Checks if attribute is a valid input#
    ######################################
    def isAtrValid(self, attribute):
        if attribute in self.options.keys():
            return (True, self.atrOptions[attribute])
        return (False, -1)

    ################################################
    #Checks if upper or lower bound are right types#
    ################################################
    def isBoundValid(self, atrValue, boundValue):
        if atrValue in range(1, 3) and type(boundValue) == str:
            return True
        if atrValue in range(3, 6) and type(boundValue) == int:
            return True
        return False

    ###################################
    #select all cities in gis.dat file#
    ###################################
    def selectAllCities(self):
        pass

    #######################################
    #unselect all cities in current filter#
    #######################################

    def unselectAllCities(self):
        self.currentlySelected = []

    def printCurrent(self):
        delimiter = "\n/**********************************************/\n"
       # print(self.dataList)
        print(delimiter)
        # print(self.dataArray)
        # print(self.dataFrame.name[1])
        print("Dictionary: ", (self.dataDict[5]))

    ##############################################
    #Sets a readable dictionary set for each name#
    ##############################################
    # DESCRIPTION: This creates a dictionary to allow easy referencing of names and matching data
    def setArrayFromFile(self):
        count = 1
        currentName = ""
        currentOther = ""
        currentDistances = []
        currentKeys = []
        for i in self.dataList:
            split = i.split(", ")
            if len(split) == 2:
                currentDistances = []
                currentName = split[0]
                (currentState, other) = self.splitState(split[1])
                (currentLatitude, other) = self.splitLatitude(other)
                (currentLongitude, other) = self.splitLongitude(other)
                currentPopulation = other
                currentOther = split[1]
                currentKeys.append(currentName)
                self.dataDict[count] = {"name": currentName,
                                        "state": currentState,
                                        "latitude": currentLatitude,
                                        "longitude": currentLongitude,
                                        "population": currentPopulation,
                                        # "other": currentOther,
                                        "distances": []}
                count += 1
                # UNNEEDED PRINT STATEMENTS FOR TESTING PURPOSES
                # print("\nName: ", currentName,
                #       "\nOther: ", currentOther)

            else:
                currentDistances += split[0].split(" ")
                if len(currentDistances) == len(currentKeys) - 1:
                    # UNNEEDED PRINT STATEMENTS FOR TESTING PURPOSES
                    # print("\nDistances Count: ", len(currentDistances),
                    #       "\nKeys Count: ", len(currentKeys),
                    #       "\nKeys: ", currentKeys,
                    #       "\nDictionary Counter: ", count)
                    for i in range(len(currentKeys) - 1):
                        self.dataDict[count - 1]["distances"].append([
                            currentKeys[i], currentDistances[i]])

        self.dataArray = np.array(self.dataList)

    #
    # Splits string to retrieve State
    def splitState(self, value):
        value = value.split("[")
        return (value[0], value[1])

    ####################################
    #Splits string to retrieve latitude#
    ####################################
    def splitLatitude(self, value):
        value = value.split(",")
        return (value[0], value[1])

    #####################################
    #Splits string to retrieve longitude#
    #####################################
    def splitLongitude(self, value):
        value = value.split("]")
        return (value[0], value[1])


def main():
    test = gis()
    # test.selectAllCities()
    # test.unselectAllCities()
    test.setArrayFromFile()

    test.printCurrent()


main()
