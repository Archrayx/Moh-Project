import numpy as np


class gis:
    atrOptions = {"name": 1, "state": 2, "latitude": 3,
                  "longitude": 4, "population": 5}
    currentlySelected = []
    dt = np.dtype([("name", str), ("state", str), ("coordinates", [
        ("latitude", np.int64), ("longitude", np.int64)]), ("population", np.int64)])

    # Ctor

    def __init__(self):
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
        self.currentlySelected = np.fromfile("gis.dat", dtype=self.dt)

    #######################################
    #unselect all cities in current filter#
    #######################################

    def unselectAllCities(self):
        self.currentlySelected = []

    def printCurrent(self):
        for i in range(len(self.currentlySelected)):
            print("Current line: %d \n %s" % (i, self.currentlySelected[i]))


def main():
    test = gis()
    test.selectAllCities()
    test.printCurrent()


main()
