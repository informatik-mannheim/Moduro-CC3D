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

from Core.CellType import CellType
from ModuroModel.CMNuUa import CMNuUa


class PASCMNuUa(CMNuUa):
    def __init__(self, sim, simthread, srcDir):
        CMNuUa.__init__(self, sim, simthread, srcDir)

    def _initModel(self):
        self.name = "PASCMNuUa"
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self._run()  # Must be the last statement.

    def _createCellTypes(self):
        cellTypes = []
        medium = CellType(name="Medium", frozen=True, minDiameter=0, maxDiameter=0,
                          growthVolumePerDay=0, nutrientRequirement=0, apoptosisTimeInDays=0,
                          volFit=1.0, surFit=1.0)

        basalmembrane = CellType(name="BasalMembrane", frozen=True, minDiameter=0, maxDiameter=0,
                                 growthVolumePerDay=0, nutrientRequirement=0, apoptosisTimeInDays=180000,
                                 volFit=1.0, surFit=1.0)

        stem = CellType(name="Stem", minDiameter=8, maxDiameter=10,
                        growthVolumePerDay=10 * self.calcVolume(10),
                        nutrientRequirement=1.0, apoptosisTimeInDays=180000,
                        volFit=0.9, surFit=0.5)

        basal = CellType(name="Basal", minDiameter=10, maxDiameter=12,
                         growthVolumePerDay=10 * self.calcVolume(12),
                         nutrientRequirement=1.0, apoptosisTimeInDays=90,
                         volFit=0.9, surFit=0.5)

        intermediate = CellType(name="Intermediate", minDiameter=12, maxDiameter=15,
                                growthVolumePerDay=20 * self.calcVolume(15),
                                nutrientRequirement=1.0, apoptosisTimeInDays=30,
                                volFit=0.9, surFit=0.1)

        umbrella = CellType(name="Umbrella", minDiameter=15, maxDiameter=19,
                            growthVolumePerDay=10 * self.calcVolume(19),
                            nutrientRequirement=1.0, apoptosisTimeInDays=10,
                            volFit=0.9, surFit=0.1)

        stem.setDescendants(0.98, [stem.id, basal.id])
        stem.setDescendants(0.01, [stem.id, stem.id])
        stem.setDescendants(0.01, [basal.id, basal.id])

        cellTypes.extend((medium, basalmembrane, stem, basal, intermediate, umbrella))

        return cellTypes
