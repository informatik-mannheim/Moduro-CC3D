import random
from Steppable.ModuroMitosisSteppable import ModuroMitosisSteppable


class GrowthMitosisSteppable(ModuroMitosisSteppable):
    def __init__(self, _simulator, model, _frequency=1):
        ModuroMitosisSteppable.__init__(self, _simulator, model, _frequency)

    def moduroStep(self, mcs):
        cells_to_divide = []
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            # TODO: extract the constant 1.3 out of code into central place
            if self.model.cellTypes[cell.type].divides and \
                    cell.volume > 1.1 * cellDict['target_Volume'] and \
                    not cellDict['necrosis']:
                cells_to_divide.append(cell)
                self.divideCellRandomOrientation(cell)

    def updateAttributes(self):
        parentCell = self.mitosisSteppable.parentCell
        childCell = self.mitosisSteppable.childCell
        parentCell.targetVolume = parentCell.targetVolume / 2
        childCell.targetVolume = parentCell.targetVolume / 2
        probOfAsym = self.model.cellTypes[parentCell.type].asym
        probOfIdenSym = self.model.cellTypes[parentCell.type].idenSym
        #probOfDiffSym = self.model.cellTypes[parentCell.type].diffSym

        prob = random.random()
        print "! MIT ! prob=", prob, ", asym=", probOfAsym, ", idensym=", probOfIdenSym
        if prob <= probOfAsym:
            childCell.type = parentCell.type + 1 # A -> A + B
        elif prob <= probOfAsym + probOfIdenSym:
            childCell.type = parentCell.type # A -> A + A
        else: # A -> B + B
            childCell.type = parentCell.type + 1
            parentCell.type += 1

        cellDict = self.getDictionaryAttribute(childCell)
        self.model.setCellAttributes(cellDict, childCell, 0)
        childCell.lambdaVolume = \
            self.execConfig.calcVolLambdaFromVolFit(cellDict['volume_lambda'])
        childCell.lambdaSurface = \
            self.execConfig.calcSurLambdaFromSurFit(cellDict['surface_lambda'])

        self.model.setCellAttributes(cellDict, parentCell, 0)
        cellDict = self.getDictionaryAttribute(childCell)
        parentCell.lambdaVolume = \
            self.execConfig.calcVolLambdaFromVolFit(cellDict['volume_lambda'])
        parentCell.lambdaSurface = \
            self.execConfig.calcSurLambdaFromSurFit(cellDict['surface_lambda'])
