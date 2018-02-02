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
from math import pi as PI, sqrt

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
        self.adhEnergy = 0.1  # Some reference value.
        self.cellTypes = []
        self.energyMatrix = []
        self.execConfig = self._createExecConfig()
        self.name = ""
        random.seed(self.execConfig.SEED)
        self.cellLifeCycleLogger = CellLifeCycleLogger(self, "Celltimes.daz")
        self._initModel()

    def _run(self):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Function ModelConfig._run'
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
        cellType = self.cellTypes[cell.type]

        cellDict['id'] = ModelConfig.cellID
        ModelConfig.cellID += 1
        cellDict['removed'] = False
        cellDict['inhibited'] = True

        cellDict['min_max_volume'] = [self.execConfig.calcVoxelVolumeFromVolume(self.execConfig.voxelDensity*cellType.minVol),
                                      self.execConfig.calcVoxelVolumeFromVolume(self.execConfig.voxelDensity*cellType.maxVol)]

        cellDict['normal_volume'] = random.uniform(cellDict['min_max_volume'][0],
                                                   cellDict['min_max_volume'][1])

        cellDict['growth_factor'] = []  # really needed?
        cellDict['life_time'] = lifeTimeParent  # How many MCS is this cell alive?


        cell.targetVolume = cell.volume + 1
        print '!!!!!!!!!!!!!!!!!!!!!!!! Cell.Volume in Voxel {} - TargetVolume {}'.format(cell.volume, cell.targetVolume)
        # TODO TMUELLER fix surface calculation
        #cell.targetSurface = self.execConfig.calcVoxelSurfaceFromVoxelVolume(cell.targetVolume)
        print '!!!!!!!!!!!!!!!!!!!!!!!! Cell.Surface in Voxel {} - TargetSurface {}'.format(cell.surface, cell.targetSurface)

        cell.lambdaVolume = 1
        cell.lambdaSurface = 3

    def _addMembrane(self, typename, xPos, yPos, zPos, xLength, yLength, zLength, steppable):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Function ModelConfig._addMembrane'
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
        steppable.cellField[
        xPosDim:xPosDim + xLengthDim - 1,
        yPosDim:yPosDim + yLengthDim - 1,
        zPosDim:zPosDim + zLengthDim - 1] = cell

    def _add3DCell(self, typename, xPos, yPos, zPos, radius, steppable):
        '''The parameters are all in micro meter
        wheras the calculated variables are in px'''

        print 'x:{}, y:{}, z:{} r:{}'.format(xPos, yPos, zPos, radius)
        cell = steppable.newCell(typename)
        xStart = self.execConfig.calcPixelFromMuMeter(xPos - radius)
        x0 = self.execConfig.calcPixelFromMuMeter(xPos)
        xEnd = self.execConfig.calcPixelFromMuMeter(xPos + radius)
        yStart = self.execConfig.calcPixelFromMuMeter(yPos - radius)
        y0 = self.execConfig.calcPixelFromMuMeter(yPos)
        yEnd = self.execConfig.calcPixelFromMuMeter(yPos + radius)
        zStart = self.execConfig.calcPixelFromMuMeter(zPos - radius)
        z0 = self.execConfig.calcPixelFromMuMeter(zPos)
        zEnd = self.execConfig.calcPixelFromMuMeter(zPos + radius)

        radiusPx = self.execConfig.calcFloatPixel(radius)
        stepLength = 1.0
        print 'steplength {}, zStart + stepLength/2 {}'.format(stepLength, (zStart+(((zStart+stepLength) - zStart)/2.)))
        print 'x:{}-{}, y:{}-{}, z:{}-{} radiusPx:{}'.format(xStart, xEnd, yStart, yEnd, zStart, zEnd, radiusPx)
        # loop over the center of each pixel to determine boundaries of the circle
        for xr in xrange(xStart, xEnd):
            for yr in xrange(yStart, yEnd):
                for zr in xrange(zStart, zEnd):
                    rd = sqrt(
                        ((xr+(((xr+stepLength) - xr)/2.)) - x0) ** 2 +
                        ((yr+(((yr+stepLength) - yr)/2.)) - y0) ** 2 +
                        ((zr+(((zr+stepLength) - zr)/2.)) - z0) ** 2)
                    if (rd <= radiusPx):
                        steppable.cellField[xr, yr, zr] = cell




    def _initCells(self, steppable):
        '''
        Initialize the tissue with cells etc. Here a urothelium with a basal membrane
        and some stem cells is created.
        :param steppable: Required to add cells dynamically.
        :return:
        '''
        # Adds the basal membrane:
        self._addMembrane(1, 0, 0, 0, self.execConfig.xLength, 2, self.execConfig.zLength, steppable)

        # Adds the stem cells throughout the basal membrane:
        '''calculate the amount of stem cells on the basal membrane
           noStemCells is the amount of stem cells'''
        cellDiameter = self.cellTypes[2].getAvgDiameter()  # cell diameter is of type float
        if self.execConfig.dimensions == 2:
            noStemCells = int(self.execConfig.xLength * 0.12 / cellDiameter)
        else:
            noStemCells = ((self.execConfig.xLength * self.execConfig.zLength) * 0.12) / (PI * (cellDiameter / 2.) ** 2)

        if noStemCells % 1 > 0.5:
            noStemCells += 1

        noStemCells = int(noStemCells)
        '''generates a random position between the cellDiameter and the ((xLength-cellDiameter)-1)
           for each stem cell
           keep some distance to the edges of the simulation field, otherwise the cell will be only half in the simulation'''
        for s in range(0, noStemCells, 1):
            xPos = random.uniform(cellDiameter, self.execConfig.xLength - 2*cellDiameter)
            zPos = random.uniform(cellDiameter, self.execConfig.zLength - 2*cellDiameter)
            if self.execConfig.dimensions == 2:
                self._addMembrane(2, xPos, 2, 0, cellDiameter, cellDiameter, 0, steppable)
            else:
                self._add3DCell(2, xPos, 7, zPos, cellDiameter/2. , steppable)

    # TODO move configure stuff to ExecConfig?
    def _configureSimulation(self):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Function ModelConfig._configureSimulation'
        self.execConfig.initPotts()
        self.execConfig.initCellTypes(self.cellTypes)
        # TODO why 15 * ...
        self.execConfig.initEnergyMatrix(self.cellTypes, self.energyMatrix, 0 * self.adhFactor)
        self.execConfig.initPlugins("VolumeFlex", "SurfaceFlex", "PixelTracker", "NeighborTracker",
                                    "ExternalPotential")
        if self.execConfig.initNutrientDiffusion:
            self.execConfig.initDiffusion(self.cellTypes[1], 0.1, 0.000015)
        # self._initCells() # not yet possible.

        return self.execConfig.getCC3D()

    # TODO abstract method
    def _createCellTypes(self):
        return None

    # TODO abstract - abstract
    def _createEnergyMatrix(self):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Function ModelConfig._createEnergyMatrix'
        """
        Creates a uniform energy matrix of adhFac numbers only.
        :param adhEnergy: The energy.
        :return:
        """
        energyMatrix = [[self.adhEnergy for x in range(self.cellTypes.__len__())]
                        for x in range(self.cellTypes.__len__())]
        print energyMatrix
        return energyMatrix

    # TODO make it an abstract method
    def _initModel(self):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Function ModelConfig._initModel'
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self.name = "ModelName"
        self._run()

    # TODO abstract method
    def _createExecConfig(self):
        return ExecConfig(self)