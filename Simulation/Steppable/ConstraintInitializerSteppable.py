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
import random

class ConstraintInitializerSteppable(ModuroSteppable):
    def __init__(self, simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, simulator, model, _frequency)

    def start(self):
        """
        Initialize all cells.
        :return:
        """
        # Required here! Otherwise CC3D will not create the file.
        #self.execConfig.parameterStore.saveParameterfile("ParameterDump.dat")
        self.execConfig.parameterStore.saveAllObjs("ParameterDump.dat")


        # Adds the basal membrane:
        self._addCubicCell(1, 0, 0, 0, self.execConfig.xLength, 2, self.execConfig.zLength)
        # Adds the stem cells throughout the basal membrane:
        self._spreadStemCells()

        for cell in self.cellList:
            # cellDict needs to be retrieved in a steppable:
            cellDict = self.getDictionaryAttribute(cell)
            self.model.initCellAttributes(cell, cellDict)
            self.model.cellLifeCycleLogger.cellLifeCycleBirth(0, cell, cellDict)

            cellType = self.model.cellTypes[cell.type]



    def _addCubicCell(self, typename, xPos, yPos, zPos, xLength, yLength, zLength):
        cell = self.newCell(typename)
        xPosDim = self.execConfig.calcPixelFromMuMeter(xPos)
        yPosDim = self.execConfig.calcPixelFromMuMeter(yPos)
        zPosDim = self.execConfig.calcPixelFromMuMeter(zPos)
        xLengthDim = self.execConfig.calcPixelFromMuMeter(xLength)
        yLengthDim = self.execConfig.calcPixelFromMuMeter(yLength)
        zLengthDim = self.execConfig.calcPixelFromMuMeter(zLength)
        # size of cell will be SIZExSIZEx1
        self.cellField[xPosDim:xPosDim + xLengthDim - 1,
        yPosDim:yPosDim + yLengthDim - 1,
        zPosDim:zPosDim + zLengthDim - 1] = cell

    def _spreadStemCells(self):
        cellDiameter = self.model.cellTypes[2].getAvgDiameter()
        stemCellFactor = 8 * cellDiameter
        if self.execConfig.dimensions == 2:
            noStemCells = int(self.execConfig.xLength / stemCellFactor)
        else:
            noStemCells = int(self.execConfig.xLength * self.execConfig.yLength /
                              (stemCellFactor * stemCellFactor))
        for s in range(1, noStemCells + 1, 1):
            xPos = random.uniform(cellDiameter, self.execConfig.xLength - cellDiameter)
            zPos = random.uniform(cellDiameter, self.execConfig.zLength - cellDiameter)
            if self.execConfig.dimensions == 2:
                self._addCubicCell(2, xPos, 2, 0, cellDiameter, cellDiameter, 0)
            else:
                self._addCubicCell(2, xPos, 2, zPos, cellDiameter,
                                   cellDiameter, cellDiameter)

