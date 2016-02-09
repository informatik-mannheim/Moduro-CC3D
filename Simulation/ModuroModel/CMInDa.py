from ModuroModel.CMInUa import CMInUa


class CMInDa(CMInUa):
    def __init__(self, sim, simthread, srcDir):
        CMInUa.__init__(self, sim, simthread, srcDir)

    def _initModel(self):
        self.name = "CMInDa"
        self.adhFactor = 0.5  # average adhesion = 0.5
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self._run()  # Must be the last statement.

    def _createEnergyMatrix(self):
        energyMatrix = [[0, 14, 14, 14, 14, 4],
                        [0, -1, 1, 3, 12, 12],
                        [0, 0, 6, 4, 8, 14],
                        [0, 0, 0, 5, 8, 12],
                        [0, 0, 0, 0, 6, 4],
                        [0, 0, 0, 0, 0, 2]]

        return energyMatrix