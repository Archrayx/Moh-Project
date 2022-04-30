from multiprocessing.sharedctypes import Value
import numpy as np
import networkx as nx
import pandas as pd
import time


class gis:
    # used to store final output of query
    final_results = []
    # used to hold current query
    currentlySelected = []
    # Alphabet List
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    # Options hashmap for selecting query options
    ATR_OPTIONS = {"name": 0, "state": 1, "latitude": 2,
                   "longitude": 3, "population": 4}

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
        tempSelected = []
        if (isAnAtr and isALowerBound and isAnUpperBound):
            if type(lowerBound) == int:
                for sublist in self.currentlySelected:
                    if any(item < lowerBound or item >= upperBound for item in sublist[atrValue]):
                        continue
                    tempSelected.append(sublist)
                print(tempSelected)
                #self.currentlySelected = tempSelected
            else:
                pass  # implement filter words in between two letters
        else:
            raise ValueError

    ######################################
    #Checks if attribute is a valid input#
    ######################################

    def isAtrValid(self, attribute):
        if attribute in self.ATR_OPTIONS.keys():
            return (True, self.ATR_OPTIONS[attribute])
        return (False, -1)

    ################################################
    #Checks if upper or lower bound are right types#
    ################################################
    def isBoundValid(self, atrValue, boundValue):
        if atrValue in range(0, 2) and type(boundValue) == str:
            return True
        if atrValue in range(2, 5) and type(boundValue) == int:
            return True
        return False

    ###################################
    #select all cities in gis.dat file#
    ###################################
    def selectAllCities(self):
        self.setArrayFromFile()
        for i in range(len(self.dataDict.keys())):
            self.currentlySelected.append([
                self.dataDict[i+1]["name"], self.dataDict[i+1]["state"], self.dataDict[i+1]["latitude"], self.dataDict[i+1]["longitude"], self.dataDict[i+1]["population"]])

    #######################################
    #unselect all cities in current filter#
    #######################################

    def unselectAllCities(self):
        self.currentlySelected = []

    #########################################################################
    #Print Methods, calls other methods that generate String to Print Result#
    #########################################################################
    def printCities(self, attribute="name", choice="S"):
        (isAnAtr, atrValue) = self.isAtrValid(attribute)
        if (isAnAtr):
            self.sortCurrentlySelected(atrValue)
            if (choice == "F"):
                finalString = self.generateStringFull()
                print(finalString)
            else:
                finalString = self.generateStringShort()
                print(finalString)
        else:
            raise ValueError

    ###################################
    #Generates a string in FULL Format#
    ###################################
    def generateStringFull(self):
        finalString = ""
        for i in range(len(self.currentlySelected)):
            finalString += str(i) + ": " + self.currentlySelected[i][0] + ", " + self.currentlySelected[i][1] + "[" + str(self.currentlySelected[
                i][2]) + "," + str(self.currentlySelected[i][3]) + "]" + str(self.currentlySelected[i][4]) + "\n"
        return finalString

    ################################
    #Generate a string SHORT Format#
    ################################
    def generateStringShort(self):
        finalString = ""
        for i in range(len(self.currentlySelected)):
            print("Name: ", self.currentlySelected[i][0],
                  "\nState: ", self.currentlySelected[i][1],
                  "\nLatitude: ", self.currentlySelected[i][2],
                  "\nLongitude", self.currentlySelected[i][3],
                  "\nPopulation", self.currentlySelected[i][4])
            finalString += str(i) + ": " + self.currentlySelected[i][0] + \
                ", " + self.currentlySelected[i][1] + "\n"
        return finalString

    ########################################
    #Uses sort method to sort sublist index#
    ########################################
    # Link: https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist/
    def sortCurrentlySelected(self, value):
        self.currentlySelected.sort(key=lambda x: x[value])

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

                currentKeys.append(currentName)
                self.dataDict[count] = {"name": currentName,
                                        "state": currentState,
                                        "latitude": int(currentLatitude),
                                        "longitude": int(currentLongitude),
                                        "population": int(currentPopulation),
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

    ##################################
    # Splits string to retrieve State#
    ##################################
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
    test.selectAllCities()
    # test.unselectAllCities()
    # test.setArrayFromFile()
    test.printCities()


main()
# Dictionary:  {'name': 'Wisconsin Dells', 'state': 'WI', 'latitude': 4363, 'longitude': 8977, 'population': 2521,
#               'distances': [['Youngstown', '1149'], ['Yankton', '1817'], ['Yakima', '481'], ['Worcester', '595']]}
