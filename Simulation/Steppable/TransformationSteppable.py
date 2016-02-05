from Steppable.ModuroSteppable import ModuroSteppable

class TransformationSteppable(ModuroSteppable):
    def __init__(self, _simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, _simulator, model, _frequency)

    def moduroStep(self, mcs):
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            cellType = self.model.cellTypes[cell.type]
            if cellType.differentiates and not cellType.divides:
                if cell.type == self.BASAL:
                    contactBasalMembrane = 0
                    for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                        if neighbor:
                            typeOfNeighbor = self.inventory.attemptFetchingCellById(neighbor.id).type
                            if typeOfNeighbor == self.BASALMEMBRANE:
                                contactBasalMembrane += commonSurfaceArea
                    if contactBasalMembrane == 0:
                        cell.type = self.INTERMEDIATE
                        self.model.setCellAttributes(cellDict, cell, cellDict['life_time'])
                elif cell.type == self.INTERMEDIATE:
                    contactMedium = 0
                    for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                        if not neighbor:
                            contactMedium += commonSurfaceArea
                    if contactMedium > 0:
                        cell.type = self.UMBRELLA
                        self.model.setCellAttributes(cellDict, cell, cellDict['life_time'])

