# Copyright 2016 the original author or authors.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

__author__ = "Markus Gumbel"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Test"

from math import pi as PI

from Core.CellType import CellType
from Core.ModelConfig import ModelConfig
from Steppable.InitializerSteppable import InitializerSteppable
from Steppable.GrowthMitosisSteppable import GrowthMitosisSteppable
from Steppable.GrowthSteppable import GrowthSteppable
from Test.Steppable.MonitorSteppable import MonitorSteppable


class VerifyGrowth(ModelConfig):
    '''
    Test classes to verify that the time and space scaling is correct.
    Two cells are put on a plane and simulated for 2 days.
    '''
    def __init__(self, sim, simthread, srcDir):
        ModelConfig.__init__(self, sim, simthread, srcDir)

    def _initModel(self):
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
                        growthVolumePerDay=1 * self.calcVolume(20),
                        nutrientRequirement=1.0, apoptosisTimeInDays=180000,
                        volFit=0.9, surFit=0.5)

        cell.setDescendants(1.0, [cell.id, cell.id])
        cellTypes.append(cell)
        return cellTypes

    def _initCells(self, steppable):
        r = self.cellTypes[1].getAvgDiameter() / 2.0
        length = PI ** (1.0 / 2.0) * r if self.execConfig.dimensions == 2 \
            else (4.0 / 3.0 * PI) ** (1.0 / 3.0) * r
        x = self.execConfig.xLength * 0.3 - length / 2.0
        y = self.execConfig.yLength * 0.3 - length / 2.0
        z = self.execConfig.zLength * 0.3 - length / 2.0 \
            if self.execConfig.dimensions == 3 else 0
        xl = length
        yl = length
        zl = 0 if self.execConfig.dimensions == 2 else length

        self._addCubicCell(1, x, y, z, xl, yl, zl, steppable)

        x = self.execConfig.xLength * 0.7 - length / 2.0
        y = self.execConfig.yLength * 0.7 - length / 2.0
        z = self.execConfig.zLength * 0.7 - length / 2.0 \
            if self.execConfig.dimensions == 3 else 0

        self._addCubicCell(1, x, y, z, xl, yl, zl, steppable)

    def _getSteppables(self):
        steppableList = []
        steppableList.append(InitializerSteppable(self.sim, self))
        steppableList.append(GrowthSteppable(self.sim, self))
        steppableList.append(GrowthMitosisSteppable(self.sim, self, splitPercentage=2.0))
        steppableList.append(MonitorSteppable(self.sim, self))

        return steppableList
