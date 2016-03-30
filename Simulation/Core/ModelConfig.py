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

    cellID = 1

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

    def _createExecConfig(self, srcDir):
        return ExecConfig(self, srcDir)


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
        # Assign a new cell ID.
        cellDict['id'] = ModelConfig.cellID
        ModelConfig.cellID += 1
        cellDict['removed'] = False

        cellDict['min_max_volume'] = [self.execConfig.calcVoxelVolumeFromVolume(cellType.minVol),
                                      self.execConfig.calcVoxelVolumeFromVolume(cellType.maxVol)]
        cellDict['normal_volume'] = random.uniform(cellDict['min_max_volume'][0],
                                                   cellDict['min_max_volume'][1])

        cellDict['growth_factor'] = [] # really needed?
        cellDict['life_time'] = lifeTimeParent  # How many MCS is this cell alive?

        cell.targetVolume = cell.volume + 1 # At the beginning, the target is the actual size.
        #cell.targetVolume = cellDict['normal_volume'] # At the beginning, the target is the actual size.
        cell.targetSurface = self.execConfig.calcVoxelSurfaceFromVoxelVolume(cell.targetVolume)
        cell.lambdaVolume = self.execConfig.calcVolLambdaFromVolFit(cellType.volFit)
        cell.lambdaSurface = self.execConfig.calcSurLambdaFromSurFit(cellType.surFit)
