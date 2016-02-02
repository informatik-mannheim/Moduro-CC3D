from XMLUtils import ElementCC3D
from math import pi as PI
from Core.ParameterStore import ParameterStore


class ExecConfig(object):
    def __init__(self,
                 srcDir="",
                 xLength=150, yLength=200, zLength=1,
                 voxelDensity=1,
                 MCSperDay=24 * 60,
                 piffInitial="Simulation/CellsInit.piff",
                 simDurationDays=720,
                 sampleIntervalInDays=0.5,
                 fluctuationAmplitude=1.0,
                 flip2DimRatio=0.5,
                 neighborOrder=1,
                 boundary_x="Periodic",
                 debugOutputFrequency=50000,
                 SEED=100):
        """

        :param srcDir:
        :param xLength:
        :param yLength:
        :param zLength:
        :param voxelDensity:
        :param MCSperHour: MC steps per Hour. Default is 60, i.e. 1 MCS = 1 min.
        :param piffInitial:
        :param simDurationDays:
        :param fluctuationAmplitude:
        :param flip2DimRatio:
        :param neighborOrder:
        :param boundary_x:
        :param debugOutputFrequency:
        :param SEED:
        :return:
        """
        self.srcDir = srcDir
        self.xLength = xLength
        self.yLength = yLength
        self.zLength = zLength
        self.voxelDensity = voxelDensity  # 1 voxel / 1 mu
        self.dimensions = 2 if zLength <= 0 else 3
        self.xDimension = self.calcPixelFromMuMeter(xLength)
        self.yDimension = self.calcPixelFromMuMeter(yLength)
        self.zDimension = 1 if self.dimensions == 2 else self.calcPixelFromMuMeter(zLength)
        self.MCSperDay = MCSperDay
        # self.deltaT = self.MCSperDay # deprecated
        self.piffInitial = piffInitial
        self.simDurationDays = simDurationDays
        self.sampleIntervalInDays = sampleIntervalInDays
        self.sampleIntervalInMCS = self.calcMCSfromDays(sampleIntervalInDays)
        self.maxSteps = self.calcMCSfromDays(simDurationDays)
        self.fluctuationAmplitude = fluctuationAmplitude
        self.flip2DimRatio = flip2DimRatio
        self.neighborOrder = neighborOrder
        self.boundary_x = boundary_x
        self.debugOutputFrequency = debugOutputFrequency
        self.SEED = SEED
        self.__cc3d = None
        self.parameterStore = ParameterStore()

    def initPotts(self):
        self.__cc3d = ElementCC3D("CompuCell3D", {"version": "3.7.3"})
        potts = self.__cc3d.ElementCC3D("Potts")
        potts.ElementCC3D("Dimensions", {"x": self.xDimension, "y": self.yDimension, "z": self.zDimension})
        potts.ElementCC3D("Steps", {}, self.maxSteps)
        potts.ElementCC3D("FluctuationAmplitude", {}, self.fluctuationAmplitude)
        potts.ElementCC3D("Flip2DimRatio", {}, self.flip2DimRatio)
        potts.ElementCC3D("NeighborOrder", {}, self.neighborOrder)
        potts.ElementCC3D("Boundary_x", {}, self.boundary_x)
        potts.ElementCC3D("DebugOutputFrequency", {}, self.debugOutputFrequency)
        potts.ElementCC3D("RandomSeed", {}, self.SEED)

    def initCellTypes(self, cellTypes):
        PluginElmnt = self.__cc3d.ElementCC3D("Plugin", {"Name": "CellType"})
        for i in range(cellTypes.__len__()):
            if cellTypes[i].frozen:
                PluginElmnt.ElementCC3D("CellType", {"Freeze": "",
                                                     "TypeId": cellTypes[i].id,
                                                     "TypeName": cellTypes[i].name})
            else:
                PluginElmnt.ElementCC3D("CellType", {"TypeId": cellTypes[i].id,
                                                     "TypeName": cellTypes[i].name})

    def initEnergyMatrix(self, cellTypes, energyMatrix, adhFactor):
        contact = self.__cc3d.ElementCC3D("Plugin", {"Name": "Contact"})
        for i in range(cellTypes.__len__()):
            for j in range(i, cellTypes.__len__()):
                contact.ElementCC3D("Energy", {"Type1": cellTypes[i].name,
                                               "Type2": cellTypes[j].name},
                                    adhFactor * energyMatrix[i][j])

    def initPlugins(self, *args):
        for a in args:
            self.__cc3d.ElementCC3D("Plugin", {"Name": a})

    def initDiffusion(self, cellType, secretionRateNutr, decayConstantNutr):
        SteppableElmnt = self.__cc3d.ElementCC3D("Steppable", {"Type": "FlexibleDiffusionSolverFE"})
        DiffusionFieldElmnt = SteppableElmnt.ElementCC3D("DiffusionField")
        DiffusionDataElmnt = DiffusionFieldElmnt.ElementCC3D("DiffusionData")
        DiffusionDataElmnt.ElementCC3D("FieldName", {}, "Nutrients")
        DiffusionDataElmnt.ElementCC3D("DiffusionConstant", {}, secretionRateNutr)
        DiffusionDataElmnt.ElementCC3D("DecayConstant", {}, decayConstantNutr)
        SecretionDataElmnt = DiffusionFieldElmnt.ElementCC3D("SecretionData")
        # TODO correct?
        SecretionDataElmnt.ElementCC3D("Secretion", {"Type": cellType.name}, secretionRateNutr * self.MCSperDay)

    def initField(self, pifText):
        fileName = "Simulation\CellsInit.piff"
        filePath = self.srcDir + "\\" + fileName

        fileHandle = open(filePath, 'w')
        fileHandle.write(pifText)
        fileHandle.close()

        PIFInitializer = self.__cc3d.ElementCC3D("Steppable", {"Type": "PIFInitializer"})
        PIFInitializer.ElementCC3D("PIFName", {}, fileName)

    def getCC3D(self):
        return self.__cc3d

    def calculateLatticeSize(self):
        return self.xDimension * self.yDimension * self.zDimension

    def interuptMCS(self, mcs):
        return (mcs == 0) or (mcs % self.sampleIntervalInMCS == 0)

    def addParameter(self, key, value):
        # TODO: ghj
        return None

    def calcPixelFromMuMeter(self, mum):
        """
        Convert a length in micro meter to a pixel length.
        This is influenced by the voxelDensity.
        :param mum:
        :return:
        """
        return self.__truncate(self.voxelDensity * mum)

    def calculateVolume(self, diameter):
        if self.dimensions == 2:
            return PI * (diameter / 2.0) ** 2  # Area
        else:
            return 4.0 / 3.0 * PI * (diameter / 2.0) ** 3  # Volume

    def calculateSurface(self, diameter):
        if self.dimensions == 2:
            return 2 * PI * (diameter / 2.0)  # Circumference
        else:
            return 4 * PI * (diameter / 2.0) ** 2  # Surface

    def calcVoxelVolumeFromVolume(self, volume):
        """
        Calculates the voxel volume from a physical volume. The results
        depends on the dimension of the simulation (2D or 3D).
        The scaling is influenced by the voxelDensity.
        :param volume: physical volume in mu m^3.
        :return: Voxel volume.
        """
        r = (3 * volume / (4 * PI)) ** (1.0 / 3)  # Radius of a sphere with known volume.
        rDimension = self.calcPixelFromMuMeter(r)  # Convert it to a pixel unit.
        if self.dimensions == 2:
            # a = self.__truncateToVoxel(PI * (rDimension ** 2))
            # if volume > 0:
            #    print "volume=", volume, ", rDim=", rDimension, ", r=", r, ", A=", a
            return self.__truncate(PI * (rDimension ** 2))  # Area of a circle.
        else:
            return self.__truncate(4.0 / 3 * PI * (rDimension ** 3))  # Volume of a sphere.

    def calcVoxelSurfaceFromVoxelVolume(self, voxelVolume):
        """
        Calculates the voxel surface from a voxel volume. The results
        depends on the dimension of the simulation (2D or 3D).
        :param voxelVolume: volume (in pixel^3).
        :return: Surface in pixel^2 ^(3D) or pixel (2).
        """
        if self.dimensions == 2:
            return self.__truncate(2 * (PI * voxelVolume) ** (1.0 / 2))  # Circumference.
        else:
            return self.__truncate(4 * PI * (3 * voxelVolume / (4 * PI)) ** (2.0 / 3))  # Surface.

    def __truncate(self, value):
        res = int(value)
        if res < 1:
            return 1  # Ensure that size is at least 1.
        else:
            return res

    def calcMCSfromDays(self, days):
        """
        Convert the time scale days into MC steps.
        :param days:
        :return:
        """
        return self.__truncate(self.MCSperDay * days)

    def calcDaysFromMCS(self, mcs):
        """
        Convert the MCS number into days.
        :param mcs:
        :return:
        """
        return mcs / (1.0 * self.MCSperDay)
