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

__author__ = "Angelo Torelli, Markus Gumbel"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Production"

import random
from Steppable.ModuroSteppable import ModuroSteppable

class GrowthSteppable(ModuroSteppable):
    def __init__(self, simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, simulator, model, _frequency)

    def moduroStep(self, mcs):
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            cellType = self.model.cellTypes[cell.type]
            # print "!!!!!! cell.tvol=", cell.targetVolume, "<=type.tVol=", cellDict['normal_volume']

            # DEPENDS ON HOW MUCH A MCS IS
            cellDict['life_time'] += 1
            if cellDict['life_time'] >= cellDict['exp_life_time']:
                cellDict['necrosis'] = True
            elif cellType.divides or cell.targetVolume <= cellDict['normal_volume']:
                cell.targetSurface = self.execConfig.calcVoxelSurfaceFromVoxelVolume(cell.volume)
                # print "! ! ! ! tSurf=", cell.targetSurface
                # Growth (mu m^3 ) per MCS:
                # deltaVolPerMCS = 1.0 * cellType.growthVolumePerDay / self.execConfig.MCSperDay
                # Volume/surface change in voxel per day.
                deltaVolDimPerDay = self.execConfig.calcVoxelVolumeFromVolume(cellType.growthVolumePerDay)
                deltaVolDimPerMCS = 1.0 * deltaVolDimPerDay / self.execConfig.MCSperDay
                if deltaVolDimPerMCS < 1.0: # The change may be too small for one MCS.
                    deltaVolDimPerMCS = 1 if deltaVolDimPerMCS >= random.random() else 0

                #print "!!::!::!:!:! deltaVol=", deltaVolPerMCS, ", deltaVolDimPerDay=",\
                #    deltaVolDimPerDay, ", deltaVolDimPerMCS=", deltaVolDimPerMCS
                cell.targetVolume += int(deltaVolDimPerMCS)
