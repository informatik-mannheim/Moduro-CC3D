from Steppable.ModuroSteppable import ModuroSteppable

class CMTransformationSteppable(ModuroSteppable):
    def __init__(self, _simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, _simulator, model, _frequency)

    def moduroStep(self, mcs):
        for cell in self.cellList:
            if cell.type == self.BASAL:
                for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                    if neighbor and neighbor.type == self.BASALMEMBRANE and commonSurfaceArea > 0:
                        break
                else:
                    cellDict = self.getDictionaryAttribute(cell)
                    cell.type = self.INTERMEDIATE
                    self.model.setCellAttributes(cellDict, cell, cellDict['life_time'])
            elif cell.type == self.INTERMEDIATE:
                for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                    if not neighbor and commonSurfaceArea > 0:
                        cellDict = self.getDictionaryAttribute(cell)
                        cell.type = self.UMBRELLA
                        self.model.setCellAttributes(cellDict, cell, cellDict['life_time'])
                        break

