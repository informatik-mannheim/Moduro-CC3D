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
from Steppable.ModuroSteppable import ModuroSteppable

class UrinationSteppable(ModuroSteppable):
    def __init__(self, _simulator,  model, prop=0.02, _frequency=1):
        ModuroSteppable.__init__(self, _simulator, model, _frequency)
        self.urinationMCS = self.execConfig.calcMCSfromDays(0.25) # every six hours.
        self.deathIntervalMCS = self.execConfig.calcMCSfromDays(1) # one day.
        self.prop = prop

    def moduroStep(self, mcs):
        if mcs > 2 * self.urinationMCS and mcs % self.urinationMCS == 0:
            # print "URINATION !!!!!!!!!!!!!!!!!!!! at ", mcs
            self._removeCells()

    def _removeCells(self):
        for cell in self.cellList:
            totalArea = 0
            cell.lambdaVecX = 0
            if random.random() < self.prop:
                for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                    if not neighbor:
                        totalArea += commonSurfaceArea
                if totalArea > 0:
                    # print "WEG!!!!!!!!!!!!!!!!!!!"
                    cellDict = self.getDictionaryAttribute(cell)
                    cellDict['necrosis'] = True
                    # TODO was happens here?
                    #cell.lambdaVecY = 0 # -500
                    #apoptosisDays = self.model.cellTypes[cell.type].apoptosisTimeInDays
                    #killTime = self.execConfig.calcMCSfromDays(apoptosisDays)
                    #cellDict['life_time'] = killTime - self.deathIntervalMCS