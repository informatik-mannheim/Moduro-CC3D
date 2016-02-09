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
        self.execConfig = self._createExecConfig(self.srcDir)
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
        CompuCellSetup.setSimulationXMLDescription(self._configureSimulation())
        CompuCellSetup.initializeSimulationObjects(self.sim, self.simthread)

        pyAttributeDictionaryAdder, dictAdder = CompuCellSetup.attachDictionaryToCells(self.sim)

        # Add Python steppables here:
        steppableRegistry = CompuCellSetup.getSteppableRegistry()
        for steppable in self._getSteppables():
            steppableRegistry.registerSteppable(steppable)

        self.execConfig.parameterStore.saveParameterfile("ParameterDump2.dat") # geht nicht!
        CompuCellSetup.mainLoop(self.sim, self.simthread, steppableRegistry)

    # TODO move configure stuff to ExecConfig?
    def _configureSimulation(self):
        self.execConfig.initPotts()
        self.execConfig.initCellTypes(self.cellTypes)
        self.execConfig.initEnergyMatrix(self.cellTypes, self.energyMatrix, 15 * self.adhFactor)
        self.execConfig.initPlugins("Volume", "Surface", "PixelTracker", "NeighborTracker",
                                    "ExternalPotential")
        # self.execConfig.initDiffusion(self, self.cellTypes[1], 0.1, 0.000015)
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

        def addCubicCell(id, typename, xPos, yPos, zPos, xLength, yLength, zLength):
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

        # Add the basal membrane:
        addCubicCell(0, "BasalMembrane", 0, 0, 0,
                     self.execConfig.xLength, 2, self.execConfig.zLength)
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
                addCubicCell(s, "Stem", xPos, 2, 0, cellDiameter, cellDiameter, 0)
            else:
                addCubicCell(s, "Stem", xPos, 2, zPos, cellDiameter, cellDiameter, cellDiameter)

    def _getPIFText(self):
        import StringIO
        fileHandle = StringIO.StringIO()
        self._initCells(fileHandle)
        text = fileHandle.getvalue()
        fileHandle.close()
        return text

    def calcVolume(self, diameter):
        return 4.0 / 3.0 * PI * (diameter / 2.0) ** 3

    # Assigns the attributes to each cell type: *0=MinVolume, *1=MaxVol, *2=SurfaceLambda, *3=VolumeLambda, *4=GrowthRate, *5=NutrientsRequirement, *6=ApoptosisTime, *7=MitosisSize, *8=DegradationRate, *9=TransformationSize
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
        cellDict['surface_lambda'] = self.execConfig.calcSurLambdaFromSurFit(cellType.surFit)
        cellDict['volume_lambda'] = self.execConfig.calcVolLambdaFromVolFit(cellType.volFit)
        cellDict['target_Volume'] = random.uniform(cellDict['min_max_volume'][0],
                                                   cellDict['min_max_volume'][1])
        cellDict['growth_factor'] = []
        cellDict['life_time'] = lifeTimeParent  # How many MCS is this cell alive?
        expLiveTime = self.execConfig.calcMCSfromDays(cellType.apoptosisTimeInDays)
        cellDict['exp_life_time'] = random.gauss(expLiveTime, expLiveTime / 10.0)
        cellDict['necrosis'] = False
        cellDict['DNA'] = [100]  # TODO remove list
        cellDict['TurnOver'] = [False]
