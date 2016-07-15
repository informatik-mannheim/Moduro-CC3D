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
from Logger.CellLifeCycleLogger import CellLifeCycleLogger


class ModelConfig(object):
    '''
    ModelConfig defines a biological simulation model. All properties in this class
    are (as good as possible) independent of the simulation technique (like GGH and CC3D).
    Right now, ModelConfig is tailored for the urothelium but it could easily be refactored
    to become tissue independent.
    '''

    cellID = 1

    def __init__(self, sim, simthread):
        '''
        :param sim:
        :param simthread:
        :return:
        '''
        self.sim = sim
        self.simthread = simthread
        self.adhFactor = 0.25  # Average adhesion strength compared to vol./surf. fits.
        self.adhEnergy = 2.0  # Some reference value.
        self.cellTypes = []
        self.energyMatrix = []
        self.execConfig = self._createExecConfig()
        self.name = ""
        random.seed(self.execConfig.SEED)
        self.cellLifeCycleLogger = CellLifeCycleLogger(self, "Celltimes.daz")
        self._initModel()

    def _initModel(self):
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self.name = "ModelName"
        self._run()

    def _run(self):
        """
        Start the simulation.
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

    def _createExecConfig(self):
        return ExecConfig(self)

    def calcVolume(self, diameter):
        return 4.0 / 3.0 * PI * (diameter / 2.0) ** 3

    def initCellAttributes(self, cell, cellDict):
        cellType = self.cellTypes[cell.type]
        expLiveTime = self.execConfig.calcMCSfromDays(cellType.apoptosisTimeInDays)
        cellDict['exp_life_time'] = random.gauss(expLiveTime, expLiveTime / 10.0)
        cellDict['necrosis'] = False
        cellDict['DNA'] = 100
        cellDict['TurnOver'] = False
        cellDict['colony'] = -1  # Default colony id.
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
        # Assign a new cell ID.
        cellDict['id'] = ModelConfig.cellID
        ModelConfig.cellID += 1
        cellDict['removed'] = False
        cellDict['inhibited'] = True

        cellDict['min_max_volume'] = [self.execConfig.calcVoxelVolumeFromVolume(cellType.minVol),
                                      self.execConfig.calcVoxelVolumeFromVolume(cellType.maxVol)]
        cellDict['normal_volume'] = random.uniform(cellDict['min_max_volume'][0],
                                                   cellDict['min_max_volume'][1])

        cellDict['growth_factor'] = []  # really needed?
        cellDict['life_time'] = lifeTimeParent  # How many MCS is this cell alive?

        cell.targetVolume = cell.volume + 1  # At the beginning, the target is the actual size.
        # cell.targetVolume = cellDict['normal_volume'] # At the beginning, the target is the actual size.
        cell.targetSurface = self.execConfig.calcVoxelSurfaceFromVoxelVolume(cell.targetVolume)
        cell.lambdaVolume = self.execConfig.calcVolLambdaFromVolFit(cellType.volFit)
        cell.lambdaSurface = self.execConfig.calcSurLambdaFromSurFit(cellType.surFit)

    def _addCubicCell(self, typename, xPos, yPos, zPos, xLength, yLength, zLength, steppable):
        '''
        Adds a cubic (rectangle or cube) cell. All values are in micro m.
        :param typename:  Type of the cell.
        :param xPos: Lower x position of the cube (in micro m).
        :param yPos: Lower y position of the cube.
        :param zPos: Lower z position of the cube.
        :param xLength: Length in x dimension (in micro m).
        :param yLength: Length in y dimension.
        :param zLength: Length in z dimension.
        :param steppable: A steppable required for to add pixels (voxels).
        :return:
        '''
        cell = steppable.newCell(typename)
        xPosDim = self.execConfig.calcPixelFromMuMeter(xPos)
        yPosDim = self.execConfig.calcPixelFromMuMeter(yPos)
        zPosDim = self.execConfig.calcPixelFromMuMeter(zPos)
        xLengthDim = self.execConfig.calcPixelFromMuMeter(xLength)
        yLengthDim = self.execConfig.calcPixelFromMuMeter(yLength)
        zLengthDim = self.execConfig.calcPixelFromMuMeter(zLength)
        # size of cell will be SIZExSIZEx1
        steppable.cellField[xPosDim:xPosDim + xLengthDim - 1,
        yPosDim:yPosDim + yLengthDim - 1,
        zPosDim:zPosDim + zLengthDim - 1] = cell

    def _initCells(self, steppable):
        '''
        Initialize the tissue with cells etc. Here a urothelium with a basal membrane
        and some stem cells is created.
        :param steppable: Required to add cells dynamically.
        :return:
        '''
        # Adds the basal membrane:
        self._addCubicCell(1, 0, 0, 0, self.execConfig.xLength, 2, self.execConfig.zLength, steppable)
        # Adds the stem cells throughout the basal membrane:
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
                self._addCubicCell(2, xPos, 2, 0, cellDiameter, cellDiameter, 0, steppable)
            else:
                self._addCubicCell(2, xPos, 2, zPos, cellDiameter,
                                   cellDiameter, cellDiameter, steppable)
