from Steppable.ModuroSteppable import ModuroSteppable

class ConstraintInitializerSteppable(ModuroSteppable):
    def __init__(self, simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, simulator, model, _frequency)

    def start(self):
        """
        Initialize all cells.
        :return:
        """
        # Required here! Otherwise CC3D will not create the file.
        #self.execConfig.parameterStore.saveParameterfile("ParameterDump.dat")
        self.execConfig.parameterStore.saveAllObjs("ParameterDump.dat")

        id = 1
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            cellType = self.model.cellTypes[cell.type]
            cell.targetVolume = self.execConfig.calcVoxelVolumeFromVolume(cellType.minVol)
            cell.lambdaVolume = self.execConfig.calcVolLambdaFromVolFit(cellType.volFit)
            cell.lambdaSurface = self.execConfig.calcSurLambdaFromSurFit(cellType.surFit)
            # print "!!!!!!!!!! type=", cellType, "tvol=", cell.targetVolume
            if cell.type == self.STEM:
                cellDict["label"] = id
                id =+ 1

            self.model.setCellAttributes(cellDict, cell, 0)



