import random
from math import pi as PI
import CompuCellSetup
from ExecConfig import ExecConfig


class ModelConfig(object):
    def __init__(self, sim, simthread):
        self.sim = sim
        self.simthread = simthread
        # dae must be declared before _createEnergyMatrix() is invoked as it used here.
        self._dae = False
        self._nutrient = False
        self.cellTypes = []
        self.energyMatrix = None
        self.adhFactor = 0.5 # Average adhesion strength compared to vol./surf. fits.
        self.adhEnergy = 1.0 # Some reference value.
        self.name = "ModelName"

    def run(self, srcDir):
        self.execConfig = self._createExecConfig(srcDir)

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
        # TODO why 10 * ...
        self.execConfig.initEnergyMatrix(self.cellTypes, self.energyMatrix, 15 * self.adhFactor)
        self.execConfig.initPlugins("Volume", "Surface", "PixelTracker", "NeighborTracker",
                                    "ExternalPotential")
        # self.execConfig.initDiffusion(self, self.cellTypes[1], 0.1, 0.000015)
        self.execConfig.initField(self._getPIFText())

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

    def _getPIFText(self):
        import StringIO
        fileHandle = StringIO.StringIO()
        membraneHeightDim = self.execConfig.calcPixelFromMuMeter(2)
        # 2D for now. TODO
        cellDiameter = self.cellTypes[2].getAvgDiameter()
        # print "cellDiameter", cellDiameter
        fileHandle.write("0 BasalMembrane 0   %(x2)s 0   %(y1)s   0   0 \n"
                         % {"x2": self.execConfig.xDimension - 1, "y1": membraneHeightDim})
        noStemCells = int(self.execConfig.xLength / (8 * cellDiameter))
        cellDiameterDim = self.execConfig.calcPixelFromMuMeter(0.8 * cellDiameter)
        deltaX = self.execConfig.xLength / noStemCells
        for s in range(1, noStemCells + 1, 1):
            xPosDim = self.execConfig.calcPixelFromMuMeter(deltaX * s - deltaX / 2)
            fileHandle.write("%(id)s Stem  %(x1)s   %(x2)s  %(y1)s   %(y2)s   0   0 \n"
                             % {"id": s, "x1": xPosDim, "x2": xPosDim + cellDiameterDim,
                                "y1": membraneHeightDim + 1,
                                "y2": membraneHeightDim + 1 + cellDiameterDim})
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
        cellType = self.cellTypes[cell.type]
        cellDict['min_max_volume'] = [self.execConfig.calcVoxelVolumeFromVolume(cellType.minVol),
                                      self.execConfig.calcVoxelVolumeFromVolume(cellType.maxVol)]
        cellDict['surface_lambda'] = self.execConfig.calcSurLambdaFromSurFit(cellType.surFit)
        cellDict['volume_lambda'] = self.execConfig.calcVolLambdaFromVolFit(cellType.volFit)
        cellDict['target_Volume'] = [random.uniform(cellDict['min_max_volume'][0],
                                                    cellDict['min_max_volume'][1])]
        cellDict['growth_factor'] = []
        cellDict['life_time'] = [lifeTimeParent]
        cellDict['necrosis'] = [False]
        cellDict['DNA'] = [100]
        cellDict['TurnOver'] = [False]
