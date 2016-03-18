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

from Steppable.ModuroSteppable import ModuroSteppable

class CMTransformationSteppable(ModuroSteppable):
    def __init__(self, _simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, _simulator, model, _frequency)

    def moduroStep(self, mcs):
        for cell in self.cellList:
            if cell.type == self.BASAL:
                for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                    if neighbor and neighbor.type == self.BASALMEMBRANE and commonSurfaceArea > 0:
                        break
                else:
                    cellDict = self.getDictionaryAttribute(cell)
                    self.model.cellLifeCycleLogger.cellLifeCycleDeath(mcs, cell, cellDict)
                    cell.type = self.INTERMEDIATE
                    self.model.setCellAttributes(cellDict, cell, cellDict['life_time'])
                    self.model.cellLifeCycleLogger.cellLifeCycleBirth(mcs, cell, cellDict)
            elif cell.type == self.INTERMEDIATE:
                for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                    if not neighbor and commonSurfaceArea > 0:
                        cellDict = self.getDictionaryAttribute(cell)
                        self.model.cellLifeCycleLogger.cellLifeCycleDeath(mcs, cell, cellDict)
                        cell.type = self.UMBRELLA
                        self.model.setCellAttributes(cellDict, cell, cellDict['life_time'])
                        self.model.cellLifeCycleLogger.cellLifeCycleBirth(mcs, cell, cellDict)
                        break

