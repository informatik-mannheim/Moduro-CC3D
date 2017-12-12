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

import random
from Steppable.GrowthSteppable import GrowthSteppable

class NutrientGrowthSteppable(GrowthSteppable):
    def __init__(self, simulator, model, _frequency=1):
        GrowthSteppable.__init__(self, simulator, model, _frequency)

    def moduroStep(self, mcs):
        self.scalarField = self.getConcentrationField('Nutrients')
        for cell in self.cellList:
            cellType = self.model.cellTypes[cell.type]
            cellDict = self.getDictionaryAttribute(cell)
            #DEPENDS ON HOW MUCH A MCS IS
            cellDict['life_time'] += 1
            apoptosisMCS = self.execConfig.calcMCSfromDays(cellType.apoptosisTimeInDays)
            if cellDict['life_time'] >= apoptosisMCS:
                cellDict['necrosis'] = [True]
            totalNutrients = 0
            #why frozen -> it only checks that cellType is not the membrane
            if not cellType.frozen:
                pixelList = self.getCellPixelList(cell)
                for pixelTrackerData in pixelList:
                    totalNutrients += self.scalarField[
                        pixelTrackerData.pixel.x, pixelTrackerData.pixel.y, pixelTrackerData.pixel.z]
                    if self.scalarField[pixelTrackerData.pixel.x,
                                        pixelTrackerData.pixel.y,
                                        pixelTrackerData.pixel.z] > cellType.consumPerCell / self.execConfig.MCSperDay:
                        self.scalarField[pixelTrackerData.pixel.x,
                                         pixelTrackerData.pixel.y,
                                         pixelTrackerData.pixel.z] -= cellType.consumPerCell / self.execConfig.MCSperDay
                    else:
                        self.scalarField[pixelTrackerData.pixel.x,
                                         pixelTrackerData.pixel.y,
                                         pixelTrackerData.pixel.z] = 0

            print '!!!!!!!!!!!!!!!!!!!!!!!!!!NutrientGrowthSteppable -> cellType.divdes or cell.targetVolume'
            print cellType.divides
            print cell.targetVolume
            print cellDict['normal_volume']

            if cellType.divides or cell.targetVolume <= cellDict['normal_volume']:
                cell.targetSurface = self.execConfig.calcVoxelSurfaceFromVoxelVolume(cell.volume)
                #TODO: necrosis trigger if to little nutrients
                if totalNutrients >= cellType.nutrientRequirement * cell.volume:
                    deltaVolDimPerDay = self.execConfig.calcVoxelVolumeFromVolume(cellType.growthVolumePerDay)
                    deltaVolDimPerMCS = 1.0 * deltaVolDimPerDay / self.execConfig.MCSperDay
                    if deltaVolDimPerMCS < 1.0: # The change may be too small for one MCS.
                        deltaVolDimPerMCS = 1 if deltaVolDimPerMCS >= random.random() else 0
                    cell.targetVolume += deltaVolDimPerMCS




