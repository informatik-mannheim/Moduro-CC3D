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

__author__ = "Markus Gumbel, Angelo Torelli"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Production"

import random
from math import pi as PI
import CompuCellSetup
from ExecConfig import ExecConfig


class ModelConfig(object):
    def __init__(self, sim, simthread, srcDir):
        self.sim = sim
        self.simthread = simthread
        self.srcDir = srcDir
        self.adhFactor = 0.5  # Average adhesion strength compared to vol./surf. fits.
        self.adhEnergy = 2.0  # Some reference value.
        self.cellTypes = []
        self.energyMatrix = []
        self.execConfig = self._createExecConfig(self.srcDir)
        self.name = ""
        random.seed(self.execConfig.SEED)
        self._initModel()

    def _initModel(self):
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self.name = "ModelName"
        self._run()

    def _run(self):
        """
        Start the simulation.
        :param srcDir: Absolute path to source file. Required for dynamic piff init.
        :return:
        """
        self.execConfig.parameterStore.addObj(self)
        for cellType in self.cellTypes:
            self.execConfig.parameterStore.addObj(cellType)

        CompuCellSetup.setSimulationXMLDescription(self._configureSimulation())
        CompuCellSetup.initializeSimulationObjects(self.sim, self.simthread)

        pyAttributeDictionaryAdder, dictAdder = CompuCellSetup.attachDictionaryToCells(self.sim)

        # Add Python steppables here:
        steppableRegistry = CompuCellSetup.getSteppableRegistry()
        for steppable in self._getSteppables():
            steppableRegistry.registerSteppable(steppable)

        CompuCellSetup.mainLoop(self.sim, self.simthread, steppableRegistry)

    # TODO move configure stuff to ExecConfig?
    def _configureSimulation(self):
        self.execConfig.initPotts()
        self.execConfig.initCellTypes(self.cellTypes)
        # TODO why 15 * ...
        self.execConfig.initEnergyMatrix(self.cellTypes, self.energyMatrix, 15 * self.adhFactor)
        self.execConfig.initPlugins("VolumeFlex", "SurfaceFlex", "PixelTracker", "NeighborTracker",
                                    "ExternalPotential")
        if self.execConfig.initNutrientDiffusion:
            self.execConfig.initDiffusion(self.cellTypes[1], 0.1, 0.000015)
        self.execConfig.initField(self._getPIFText())
        # self._initCells() # not yet possible.

        return self.execConfig.getCC3D()

    def _createCellTypes(self):
        return None

    def _createEnergyMatrix(self):
        """
        Creates a uniform energy matrix of adhFac numbers only.
        :param adhEnergy: The energy.
        :return:
        """
        energyMatrix = [[self.adhEnergy for x in range(self.cellTypes.__len__())]
                        for x in range(self.cellTypes.__len__())]
        return energyMatrix

    def _createExecConfig(self, srcDir):
        return ExecConfig(self, srcDir)

    def _addCubicCell(self, id, typename, xPos, yPos, zPos, xLength, yLength, zLength,
                      fileHandle):
        # TODO exact?
        xPosDim = self.execConfig.calcPixelFromMuMeter(xPos)
        yPosDim = self.execConfig.calcPixelFromMuMeter(yPos)
        zPosDim = self.execConfig.calcPixelFromMuMeter(zPos)
        xLengthDim = self.execConfig.calcPixelFromMuMeterMin1(xLength)
        yLengthDim = self.execConfig.calcPixelFromMuMeterMin1(yLength)
        zLengthDim = self.execConfig.calcPixelFromMuMeterMin1(zLength)
        fileHandle.write("%(id)s %(name)s  %(x1)s   %(x2)s  %(y1)s   %(y2)s   %(z1)s   %(z2)s \n"
                         % {"id": id, "name": typename,
                            "x1": xPosDim, "x2": xPosDim + xLengthDim - 1,
                            "y1": yPosDim, "y2": yPosDim + yLengthDim - 1,
                            "z1": zPosDim, "z2": zPosDim + zLengthDim - 1})

    def _initCells(self, fileHandle):
        def addCubicCell2(typename, xPos, yPos, zPos, xLength, yLength, zLength):
            cell = self.sim.newCell(typename)
            xPosDim = self.execConfig.calcPixelFromMuMeter(xPos)
            yPosDim = self.execConfig.calcPixelFromMuMeter(yPos)
            zPosDim = self.execConfig.calcPixelFromMuMeter(zPos)
            xLengthDim = self.execConfig.calcPixelFromMuMeter(xLength)
            yLengthDim = self.execConfig.calcPixelFromMuMeter(yLength)
            zLengthDim = self.execConfig.calcPixelFromMuMeter(zLength)
            # size of cell will be SIZExSIZEx1
            self.sim.cellField[xPosDim:xPosDim + xLengthDim - 1,
            yPosDim:yPosDim + yLengthDim - 1,
            zPosDim:zPosDim + zLengthDim - 1] = cell

        # Add the basal membrane:
        self._addCubicCell(0, "BasalMembrane", 0, 0, 0,
                           self.execConfig.xLength, 2, self.execConfig.zLength, fileHandle)
        cellDiameter = self.cellTypes[2].getAvgDiameter()
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
                self._addCubicCell(s, "Stem", xPos, 2, 0, cellDiameter, cellDiameter, 0, fileHandle)
            else:
                self._addCubicCell(s, "Stem", xPos, 2, zPos, cellDiameter,
                                   cellDiameter, cellDiameter, fileHandle)

    def _getPIFText(self):
        import StringIO
        fileHandle = StringIO.StringIO()
        self._initCells(fileHandle)
        text = fileHandle.getvalue()
        fileHandle.close()
        return text

    def calcVolume(self, diameter):
        return 4.0 / 3.0 * PI * (diameter / 2.0) ** 3

    def initCellAttributes(self, cell, cellDict):
        cellType = self.cellTypes[cell.type]
        expLiveTime = self.execConfig.calcMCSfromDays(cellType.apoptosisTimeInDays)
        cellDict['exp_life_time'] = random.gauss(expLiveTime, expLiveTime / 10.0)
        cellDict['necrosis'] = False
        cellDict['DNA'] = [100]  # TODO remove list
        cellDict['TurnOver'] = [False]
        self.setCellAttributes(cellDict, cell, 0)

    def setCellAttributes(self, cellDict, cell, lifeTimeParent):
        """
        Set attributes for a cell's dictionary.
        :param cellDict:
        :param cell:
        :param lifeTimeParent:
        :return:
        """
        # cellDict = cell.getDictionaryAttribute(cell)
        cellType = self.cellTypes[cell.type]
        cellDict['min_max_volume'] = [self.execConfig.calcVoxelVolumeFromVolume(cellType.minVol),
                                      self.execConfig.calcVoxelVolumeFromVolume(cellType.maxVol)]
        cellDict['normal_volume'] = random.uniform(cellDict['min_max_volume'][0],
                                                   cellDict['min_max_volume'][1])
        cellDict['growth_factor'] = [] # really needed?
        cellDict['life_time'] = lifeTimeParent  # How many MCS is this cell alive?

        #cell.targetVolume = cell.volume # At the beginning, the target is the actual size.
        cell.targetSurface = self.execConfig.calcVoxelSurfaceFromVoxelVolume(cell.targetVolume)
        cell.lambdaVolume = self.execConfig.calcVolLambdaFromVolFit(cellType.volFit)
        cell.lambdaSurface = self.execConfig.calcSurLambdaFromSurFit(cellType.surFit)
