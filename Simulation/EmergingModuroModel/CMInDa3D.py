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

__author__ = "Markus Gumbel, Angelo Torelli"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Production"

from Core.ExecConfig import ExecConfig
from ModuroModel.CMInDa import CMInDa
from Core.CellType import CellType

class CMInDa3D(CMInDa):

    def __init__(self, sim, simthread, srcDir):
        CMInDa.__init__(self, sim, simthread, srcDir)

    def _initModel(self):
        self.name = "CMInDa3D"
        self.adhFactor = 0.1
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self._run()  # Must be the last statement.

    def _createExecConfig(self, srcDir):
        return ExecConfig(srcDir=srcDir,
                          xLength=100, yLength=120, zLength=50, voxelDensity=1,
                          MCSperDay=500,
                          fluctuationAmplitude=10.0)
