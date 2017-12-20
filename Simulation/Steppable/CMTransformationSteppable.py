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
from Steppable.TransformationSteppable import TransformationSteppable

class CMTransformationSteppable(TransformationSteppable):
    def __init__(self, _simulator, model, _frequency=1):
        TransformationSteppable.__init__(self, _simulator, model, _frequency)


    def moduroStep(self, mcs):
        for cell in self.cellList:
            #if a basal cell looses contact to the membrane
            if cell.type == self.BASAL and not self.hasCertainNeighbor(cell, self.BASALMEMBRANE):
                self.transformInto(cell, self.INTERMEDIATE, mcs)
            #if a intermediate cell
            elif cell.type == self.INTERMEDIATE and self.hasCertainNeighbor(cell, self.MEDIUM):
                self.transformInto(cell, self.UMBRELLA, mcs)

            elif (cell.type == self.STEM or cell.type == self.UMBRELLA) and self.hasCertainNeighbor(cell, self.MEDIUM):
                self.setInhibitionFlag(cell, False)


#    def hasCertainNeighbor(self, cell, neighborType):
#        totalMediumArea = 0
#        hasCertainNeighbor = False
#        for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
#            if neighbor and neighborType != 0 and neighbor.type == neighborType and commonSurfaceArea > 0:
#                hasCertainNeighbor = True
#            elif not neighbor and commonSurfaceArea > 0:
#                totalMediumArea += commonSurfaceArea
#                if neighborType == 0:
#                    hasCertainNeighbor = True
#                if hasCertainNeighbor:
#                    break
#        if totalMediumArea == 0:
#            self.setInhibitionFlag(cell, True)
#        else:
#            self.setInhibitionFlag(cell, False)
#        return hasCertainNeighbor
#
#
#    def transformInto(self, cell, cellType, mcs):
#        cellDict = self.getDictionaryAttribute(cell)
#        self.model.cellLifeCycleLogger.cellLifeCycleDeath(mcs, cell, cellDict)
#        cell.type = cellType
#        self.model.setCellAttributes(cellDict, cell, 0)
#        self.model.cellLifeCycleLogger.cellLifeCycleBirth(mcs, cell, cellDict)
#
#
#    def setInhibitionFlag(self, cell, flag):
#        cellDict = self.getDictionaryAttribute(cell)
#        cellDict['inhibited'] = flag