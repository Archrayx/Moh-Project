class gis:
    atrOptions = {"name": 1, "state": 2, "latitude": 3,
                  "longitude": 4, "population": 5}
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
        pass

    def isAtrValid(self, attribute):
        if attribute in self.options.keys():
            return (True, self.atrOptions[attribute])
        return (False, -1)

    def isBoundValid(self, atrValue, lowerBound):
        if atrValue == 1 or atrValue == 2 & & typeof(lowerBound) == str:
            return True
        return False
