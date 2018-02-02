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
from math import pi as PI, sqrt
import random

class InitializerSteppable(ModuroSteppable):
    def __init__(self, simulator, model, _frequency=1):
        print'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! in Konstruktor von InitializerSteppable'
        ModuroSteppable.__init__(self, simulator, model, _frequency)

    def start(self):
        """
        Initialize all cells after the simulation has been initialized.
        :return:
        """
        # Required here! Otherwise CC3D will not create the file.
        #self.execConfig.parameterStore.saveParameterfile("ParameterDump.dat")
        self.execConfig.parameterStore.saveAllObjs("ParameterDump.dat")
        print'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! in InitializerSteppable.start()'
        self.model._initCells(self)
        #self._initCells(self)
        for cell in self.cellList:
            # cellDict needs to be retrieved in a steppable:
            cellDict = self.getDictionaryAttribute(cell)
            self.model.initCellAttributes(cell, cellDict)
            self.model.cellLifeCycleLogger.cellLifeCycleBirth(0, cell, cellDict)

            cellType = self.model.cellTypes[cell.type]




    def _addClusterCell(self, typename, xPos, yPos, zPos, radius, steppable):
        '''Tryout to create a sphere cell as a cluster of cuboids'''
        xStart = self.execConfig.calcPixelFromMuMeter(xPos - radius)
        x0 = self.execConfig.calcPixelFromMuMeter(xPos)
        xEnd = self.execConfig.calcPixelFromMuMeter(xPos + radius)
        yStart = self.execConfig.calcPixelFromMuMeter(yPos - radius)
        y0 = self.execConfig.calcPixelFromMuMeter(yPos)
        yEnd = self.execConfig.calcPixelFromMuMeter(yPos + radius)
        zStart = self.execConfig.calcPixelFromMuMeter(zPos - radius)
        z0 = self.execConfig.calcPixelFromMuMeter(zPos)
        zEnd = self.execConfig.calcPixelFromMuMeter(zPos + radius)
        radiusPx = self.execConfig.calcPixelFromMuMeter(radius)

        cellClusterId=1

        stepLength = 1.0
        for xr in xrange(xStart, xEnd):
            for yr in xrange(yStart, yEnd):
                for zr in xrange(zStart, zEnd):
                    rd = sqrt(
                        ((xr+(((xr+stepLength) - xr)/2.)) - x0) ** 2 +
                        ((yr+(((yr+stepLength) - yr)/2.)) - y0) ** 2 +
                        ((zr+(((zr+stepLength) - zr)/2.)) - z0) ** 2)
                    if (rd <= radiusPx):
                        cell = steppable.newCell(typename)
                        steppable.cellField[xr, yr, zr] = cell
                        reassignIdFlag = self.inventory.reassignClusterId(cell, 550)

    def _initCells(self, steppable):
        self._addClusterCell(2, 30, 10, 10, 3, steppable)
