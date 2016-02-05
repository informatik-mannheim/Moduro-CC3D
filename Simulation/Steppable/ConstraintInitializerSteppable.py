from Steppable.ModuroSteppable import ModuroSteppable

class ConstraintInitializerSteppable(ModuroSteppable):
    def __init__(self, simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, simulator, model, _frequency)

    def start(self):
        """
        Initialize all cells.
        :return:
        """
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            print"!!!!!!!!!!!", cell.type
            cellType = self.model.cellTypes[cell.type]
            cell.targetVolume = self.execConfig.calcVoxelVolumeFromVolume(cellType.minVol)
            cell.lambdaVolume = self.execConfig.calcVolLambdaFromVolFit(cellType.volFit)
            cell.lambdaSurface = self.execConfig.calcSurLambdaFromSurFit(cellType.surFit)
            # print "!!!!!!!!!! type=", cellType, "tvol=", cell.targetVolume
            self.model.setCellAttributes(cellDict, cell, 0)



