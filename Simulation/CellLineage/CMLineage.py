__author__ = 'Angelo'
import random

class CMLineage(object):

    def __init__(self, model):
        self.model = model
        self.cellTypes = model.cellTypes

    def differentiates(self, celltype):
        return {
            "Basal": True,
            "Intermediate": True
        }.get(celltype.name, False)

    def divides(self, celltype):
        return {
            "Stem": True
        }.get(celltype.name, False)

    def getDescendants(self, celltype):
        return {
            "Stem": self.getStemCellDescendants(),
            "Basal": self.getCellTypeID("Intermediate"),
            "Intermediate": self.getCellTypeID("Umbrella"),
        }.get(celltype.name)


    def getStemCellDescendants(self):
        probOfAsym = 0.8
        probOfIdenSym = 0.1
        probOfDiffSym = 0.1
        prob = random.random()

        if prob < probOfAsym:
            return [self.getCellTypeID("Stem"), self.getCellTypeID("Basal")]
        elif prob < probOfAsym + probOfIdenSym:
            return [self.getCellTypeID("Stem"), self.getCellTypeID("Stem")]
        elif prob < probOfAsym + probOfIdenSym + probOfDiffSym:
            return [self.getCellTypeID("Basal"), self.getCellTypeID("Basal")]


    def getCellTypeID(self, name):
        for i in range(self.cellTypes.__len__()):
            if self.cellTypes[i].name == name:
                return self.cellTypes[i].id


