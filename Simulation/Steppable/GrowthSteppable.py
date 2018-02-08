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
    def __init__(self, simulator, model, contactInhibitedFactor=50.0,_frequency=1):
        ModuroSteppable.__init__(self, simulator, model, _frequency)
        self.contactInhibitedFactor = contactInhibitedFactor    #um wie viel wachsen die zellen schneller

    def moduroStep(self, mcs):
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            cellType = self.model.cellTypes[cell.type]

            cellDict['life_time'] += 1
            if cellDict['life_time'] >= cellDict['exp_life_time']:
                cellDict['necrosis'] = True

                #if cellType.divides is false than second part otherwise cellType.divides
            elif cellType.divides or cell.targetVolume <= cellDict['normal_volume']:
                if cellDict['inhibited']:   #if there enough other cells around than the inhibited cell will grow normal and not faster
                    growthVolPerDay = cellType.growthVolumePerDay
                else:
                    growthVolPerDay = cellType.growthVolumePerDay * self.contactInhibitedFactor

                deltaVolDimPerDay = self.execConfig.calcVoxelVolumeFromVolume(growthVolPerDay)
                deltaVolDimPerMCS = 1.0 * deltaVolDimPerDay / self.execConfig.MCSperDay

                # if the growth is to small, take a random number between 0 and 1 -> maybe add the pixel or not
                if deltaVolDimPerMCS < 1.0: # The change may be too small for one MCS.
                    deltaVolDimPerMCS = 1 if deltaVolDimPerMCS >= random.random() else 0

                # reduce the approximation error
                if deltaVolDimPerMCS % 1.0 > 0.5:
                    deltaVolDimPerMCS += 1

                cell.targetVolume += int(deltaVolDimPerMCS)
                cell.targetSurface = self.execConfig.calcVoxelSurfaceFromVoxelVolume(cell.targetVolume)
