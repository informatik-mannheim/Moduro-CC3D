from math import pi as PI

from Core.CellType import CellType
from Core.ExecConfig import ExecConfig
from Core.ModelConfig import ModelConfig
from Steppable.ConstraintInitializerSteppable import ConstraintInitializerSteppable
from Test.Steppable.MonitorSteppable import MonitorSteppable


class SphereTest(ModelConfig):
    '''
    Some experiments on a cell's shape.
    '''
    def __init__(self, sim, simthread, srcDir):
        ModelConfig.__init__(self, sim, simthread, srcDir)

    def _initModel(self):
        self.name = "SphereTest"
        self.adhFactor = 0.5  # average adhesion = 0.5
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self._run()  # Must be the last statement.

    def _createCellTypes(self):
        cellTypes = []

        medium = CellType(name="Medium", frozen=True, minDiameter=0, maxDiameter=0,
                          growthVolumePerDay=0, nutrientRequirement=0, apoptosisTimeInDays=0,
                          volFit=1.0, surFit=1.0)
        cellTypes.append(medium)

        cell = CellType(name="Cell", minDiameter=20, maxDiameter=20,
                        growthVolumePerDay=10 * self.calcVolume(10),
                        nutrientRequirement=1.0, apoptosisTimeInDays=180000,
                        volFit=0.9, surFit=0.5, divides=True)
        cellTypes.append(cell)
        return cellTypes

    def _initCells(self, fileHandle):
        r = self.cellTypes[1].getAvgDiameter() / 2.0
        length = PI ** (1.0 / 2.0) * r if self.execConfig.dimensions == 2 \
            else (4.0 / 3.0 * PI) ** (1.0 / 3.0) * r
        x = self.execConfig.xLength * 0.3 - length / 2.0
        y = self.execConfig.yLength * 0.3 - length / 2.0
        z = self.execConfig.zLength * 0.3 - length / 2.0 \
            if self.execConfig.dimensions == 3 else 0
        xl = length
        yl = length
        zl = 1 if self.execConfig.dimensions == 2 else length

        self._addCubicCell(0, "Cell", x, y, z, xl, yl, zl, fileHandle)

        x = self.execConfig.xLength * 0.7 - length / 2.0
        y = self.execConfig.yLength * 0.7 - length / 2.0
        z = self.execConfig.zLength * 0.7 - length / 2.0 \
            if self.execConfig.dimensions == 3 else 0

        self._addCubicCell(1, "Cell", x, y, z, xl, yl, zl, fileHandle)

    def _getSteppables(self):
        steppableList = []
        steppableList.append(ConstraintInitializerSteppable(self.sim, self))
        steppableList.append(MonitorSteppable(self.sim, self))

        return steppableList

    def _createExecConfig(self, srcDir):
        return ExecConfig(srcDir=srcDir,
                          xLength=70, yLength=70, zLength=70, voxelDensity=.5)
