from Steppable.ModuroMitosisSteppable import ModuroMitosisSteppable


class GrowthMitosisSteppable(ModuroMitosisSteppable):
    def __init__(self, _simulator, model, _frequency=1):
        ModuroMitosisSteppable.__init__(self, _simulator, model, _frequency)

    def moduroStep(self, mcs):
        cells_to_divide = []
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            cellType = self.model.cellTypes[cell.type]

            # TODO: extract the constant 1.3 out of code into central place
            if cellType.divides and \
                    cell.volume > 1.3 * cellDict['target_Volume'] and \
                    not cellDict['necrosis']:
                cells_to_divide.append(cell)
                self.divideCellRandomOrientation(cell)

    def updateAttributes(self):
        parentCell = self.mitosisSteppable.parentCell
        childCell = self.mitosisSteppable.childCell
        parentCell.targetVolume = parentCell.targetVolume / 2
        childCell.targetVolume = parentCell.targetVolume / 2

        descendents = self.model.cellTypes[parentCell.type].getDescendants()
        parentCell.type = descendents[0].id
        childCell.type = descendents[1].id

        # Now set the attributes for the two daughter cells:
        cellDict = self.getDictionaryAttribute(childCell)
        self.model.setCellAttributes(cellDict, childCell, 0)
        childCell.lambdaVolume = \
            self.execConfig.calcVolLambdaFromVolFit(cellDict['volume_lambda'])
        childCell.lambdaSurface = \
            self.execConfig.calcSurLambdaFromSurFit(cellDict['surface_lambda'])

        self.model.setCellAttributes(cellDict, parentCell, 0)
        cellDict = self.getDictionaryAttribute(parentCell)
        parentCell.lambdaVolume = \
            self.execConfig.calcVolLambdaFromVolFit(cellDict['volume_lambda'])
        parentCell.lambdaSurface = \
            self.execConfig.calcSurLambdaFromSurFit(cellDict['surface_lambda'])
