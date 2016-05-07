import numpy as np
from biochemistry import *
import numpy as np

class Operator:
    greater, smaller, equal, nequal = range(4)
    mapping = {"greater": greater, "smaller": smaller, "equal": equal, "not equal": nequal}

    def compare(self, value1, value2, operator):
        if operator == self.greater:
            return (value1 > value2)
        elif operator == self.smaller:
            return (value1 < value2)
        elif operator == self.equal:
            return (value1 == value2)
        elif operator == self.nequal:
            return (value1 != value2)

class FrameFilter:
    def __init__(self,name):
        self.name = name

    def extractFrameRange(self, contacts, range):
        lower = range[0]
        upper = range[1]
        for c in contacts:
            newScores = c.scoreArray[lower:upper]
            c.scoreArray = newScores
        return contacts

class NameFilter:
    def __init__(self, name):
        self.name = name

    def filterResiduesByName(self, contacts, resnameA, resnameB):
        filtered = []
        for c in contacts:
            add = False
            if resnameA.lower() != 'all' and resnameB.lower() != 'all':
                splitA = resnameA.split(",")
                splitB = resnameB.split(",")
                if c.residueA.name in splitA and c.residueB.name in splitB:
                    add = True
            elif resnameA.lower() != 'all' and resnameB.lower() == 'all':
                splitA = resnameA.split(",")
                if c.residueA.name in splitA:
                    add = True
            elif resnameA.lower() == 'all' and resnameB.lower() != 'all':
                splitB = resnameB.split(",")
                if c.residueB.name in splitB:
                    add = True
            else:
                add = True

            if add:
                filtered.append(c)
        return filtered

class ResidueRangeFilter:
    def __init__(self, name):
        self.name = name

    def numberInRanges(self,number,ranges):
        result = False
        for r in ranges:
            if number in r:
                result = True
        return result

    def filterResiduesByRange(self, contacts, residRangeA, residRangeB):
        splitA = residRangeA.split(",")
        splitB = residRangeB.split(",")

        notAllA = residRangeA.lower() != 'all'
        notAllB = residRangeB.lower() != 'all'

        if notAllA:
            aRanges = []
            for ran in splitA:
                r = ran.split("-")
                aRanges.append(range(int(r[0]),int(r[1])+1))
        if notAllB:
            bRanges =[]
            for ran in splitB:
                r = ran.split("-")
                print(r)
                bRanges.append(range(int(r[0]), int(r[1]) + 1))

        filtered = []
        for c in contacts:
            add = False
            if notAllA and notAllB:
                if self.numberInRanges(c.residueA.ident, aRanges) and self.numberInRanges(c.residueB.ident,bRanges):
                    add = True
            elif notAllA and not notAllB:
                if self.numberInRanges(c.residueA.ident, aRanges):
                    add = True
            elif not notAllA and notAllB:
                if self.numberInRanges(c.residueB.ident,bRanges):
                    add = True
            else:
                add = True

            if add:
                filtered.append(c)
        return filtered

class BinaryFilter:
    def __init__(self, name, operator, value):
        self.name = name
        self.operator = Operator.mapping[operator]
        self.value = value

    def filterContacts(self,contacts):
        pass


class TotalTimeFilter(BinaryFilter):
    def __init__(self,name, operator, value):
        super(TotalTimeFilter, self).__init__(name, operator, value)

    def filterContacts(self,contacts):
        filtered = []
        op = Operator()
        for c in contacts:
            if op.compare(c.total_time(1, 0), self.value, self.operator):
                filtered.append(c)
        print(str(len(filtered)))
        return filtered

# filter compares contact score of every frame, only adds contact if true for all frames
class ScoreFilter(BinaryFilter):
    def __init__(self, name, operator, value, ftype):
        super(ScoreFilter, self).__init__(name, operator, value)
        self.ftype = ftype

    def filterContacts(self, contacts):
        filtered = []
        op = Operator()
        if self.ftype == "mean":
            for c in contacts:
                mean = c.mean_score()
                if op.compare(mean, self.value, self.operator):
                    filtered.append(c)
        elif self.ftype == "median":
            for c in contacts:
                med = c.median_score()
                if op.compare(med, self.value, self.operator):
                    filtered.append(c)
        return filtered

class SortingOrder:
    ascending, descending = range(2)
    mapping = {"asc": ascending, "desc": descending}

class Sorting:
    def __init__(self, name, key, descending):
        self.name = name
        self. key = key
        self.descending = descending

    def setThresholdAndNsPerFrame(self,threshold,nspf):
        self.threshold = threshold
        self.nspf = nspf

    def sortContacts(self, contacts):
        sortedContacts = []
        if self.key == "mean":
            sortedContacts = sorted(contacts, key=lambda c: c.meanScore, reverse=self.descending)
        elif self.key == "median":
            sortedContacts = sorted(contacts, key=lambda c: c.medianScore, reverse=self.descending)
        elif self.key == "bb/sc type":
            sortedContacts = sorted(contacts, key=lambda c: c.backboneSideChainType, reverse=self.descending)
        elif self.key == "contact type":
            sortedContacts = sorted(contacts, key=lambda c: c.contactType, reverse=self.descending)
        elif self.key == "resid A":
            sortedContacts = sorted(contacts, key=lambda c: c.residueA.ident, reverse=self.descending)
        elif self.key == "resid B":
            sortedContacts = sorted(contacts, key=lambda c: c.residueB.ident, reverse=self.descending)
        elif self.key == "total time":
            for con in contacts:
                con.total_time(self.nspf,self.threshold)
            sortedContacts = sorted(contacts, key=lambda c: c.ttime, reverse=self.descending)
        elif self.key == "mean lifetime":
            for con in contacts:
                con.mean_life_time(self.nspf, self.threshold)
            sortedContacts = sorted(contacts, key=lambda c: c.meanLifeTime, reverse=self.descending)
        elif self.key == "median lifetime":
            for con in contacts:
                con.median_life_time(self.nspf, self.threshold)
            sortedContacts = sorted(contacts, key=lambda c: c.medianLifeTime, reverse=self.descending)
        return sortedContacts

class WeightFunction:
    def __init__(self, name, x):
        self.name = name
        self.x = x

    def weightContactFrames(self, contacts):
        for c in contacts:
            weighted = self.function(self.x) * c.scoreArray
            c.scoreArray = weighted
        return contacts

    def previewFunction(self):
        return self.function(self.x)

    def function(self, x):
        pass

class SigmoidWeightFunction(WeightFunction):
    # x: x values
    # x0: turning point
    # L: upper limit
    # k: "slope"
    def __init__(self, name, x, x0, L, k, y0):
        super(SigmoidWeightFunction, self).__init__(name, x)
        self.x0 = x0
        self.L = L
        self.k = k
        self.y0 = y0

    def function(self,x):
        y = (self.L)/(1+np.exp(-self.k*(x-self.x0))) + self.y0
        return y

    def previewFunction(self):
        return self.function(self.x)


class RectangularWeightFunction(WeightFunction):
    #x: x values
    #x0: lower rect limit x value
    #x1: upper rect limit x value
    #h: rectangle height
    def __init__(self, name, x, x0, x1, h, y0):
        super(RectangularWeightFunction, self).__init__(name, x)
        self.x0 = x0
        self.x1 = x1
        self.h = h
        self.y0 = y0

    def function(self, x):
        y = np.zeros(len(x))
        y.fill(self.y0)
        y[self.x0:self.x1] = self.h
        return y

class LinearWeightFunction(WeightFunction):
    #x: x values
    #x0: lower rect limit x value
    #x1: upper rect limit x value
    #h: rectangle height
    def __init__(self, name, x, f0, f1):
        super(LinearWeightFunction, self).__init__(name, x)
        self.f0 = f0
        self.f1 = f1

    def function(self, x):
        a = (self.f1-self.f0)/x[-1]
        y = a * x + self.f0
        return y

class FunctionType:
    sigmoid, rect, linear = range(3)