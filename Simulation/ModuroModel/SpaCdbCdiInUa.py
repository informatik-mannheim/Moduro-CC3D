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

__author__ = "Angelo Torelli"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Production"

from Core.CellType import *
from Core.ExecConfig import ExecConfig
from ModuroModel.SdCdbCdiInUa import SdCdbCdiInUa


class SpaCdbCdiInUa(SdCdbCdiInUa):
    def __init__(self, sim, simthread):
        SdCdbCdiInUa.__init__(self, sim, simthread)

    def _initModel(self):
        self.name = "SpaCdbCdiInUa"
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self._run()  # Must be the last statement.

    def _createCellTypes(self):
        cellTypes = []

        stem = Stemcell
        stem.setGrowthVolumePerDayRelVolume(10.0)

        basal = Basalcell
        basal.setGrowthVolumePerDayRelVolume(10.0)
        basal.apoptosisTimeInDays = 90.0

        intermediate = Intermediatecell
        intermediate.setGrowthVolumePerDayRelVolume(20.0)
        intermediate.apoptosisTimeInDays = 30.0

        umbrella = Umbrellacell
        umbrella.setGrowthVolumePerDayRelVolume(10.0)
        umbrella.apoptosisTimeInDays = 10.0

        stem.setDescendants(1.0, [stem.id, basal.id])

        stem.setDescendants(0.98, [stem.id, basal.id])
        stem.setDescendants(0.01, [stem.id, stem.id])
        stem.setDescendants(0.01, [basal.id, basal.id])

        cellTypes.extend((Medium, Basalmembrane, stem, basal, intermediate, umbrella))

        return cellTypes


    def _createExecConfig(self):
        return ExecConfig(xLength=800, yLength=150, zLength=0, voxelDensity=0.8,
                          MCSperDay=500)
