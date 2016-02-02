import random
from Steppable.ModuroMitosisSteppable import ModuroMitosisSteppable


class GrowthMitosisSteppable(ModuroMitosisSteppable):
    def __init__(self, _simulator, execConfig, model, _frequency=1):
        ModuroMitosisSteppable.__init__(self, _simulator, execConfig, model, _frequency)

    def moduroStep(self, mcs):
        cells_to_divide = []
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            # TODO: extract the constant 1.3 out of code into central place
            if self.model.cellTypes[cell.type].differentiates and \
                    cell.volume > 1.3 * cellDict['target_Volume'][0] and \
                    not cellDict['necrosis'][0]:
                cells_to_divide.append(cell)
                self.divideCellRandomOrientation(cell)

    def updateAttributes(self):
        parentCell = self.mitosisSteppable.parentCell
        childCell = self.mitosisSteppable.childCell
        parentCell.targetVolume = parentCell.targetVolume / 2
        childCell.targetVolume = parentCell.targetVolume / 2
        prob = random.random()
        probOfAsym = self.model.cellTypes[parentCell.type].asym
        probOfIdenSym = self.model.cellTypes[parentCell.type].idenSym
        probOfDiffSym = self.model.cellTypes[parentCell.type].diffSym

        if prob < probOfAsym:
            childCell.type = parentCell.type + 1
        elif prob < probOfAsym + probOfIdenSym:
            childCell.type = parentCell.type
        elif prob < probOfAsym + probOfIdenSym + probOfDiffSym:
            childCell.type = parentCell.type + 1
            parentCell.type += 1

        cellDict = self.getDictionaryAttribute(childCell)
        self.model.setCellAttributes(cellDict, childCell, 0)
        childCell.lambdaVolume = cellDict['volume_lambda'][0]
        childCell.lambdaSurface = cellDict['surface_lambda'][0]
