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

from XMLUtils import ElementCC3D
from math import pi as PI
import time
from Core.ParameterStore import ParameterStore


class ExecConfig(object):
    def __init__(self,
                 xLength=150, yLength=200, zLength=50,
                 voxelDensity=1,
                 initNutrientDiffusion = False,
                 MCSperDay=500,
                 simDurationDays=720,
                 sampleIntervalInDays=0.5,
                 fluctuationAmplitude=10.0,
                 flip2DimRatio=0.5,
                 neighborOrder=1,
                 boundary_x="Periodic",
                 debugOutputFrequency=50000,
                 SEED=-1):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Konstruktor ExecConfig'

        """

        :param xLength:
        :param yLength:
        :param zLength:
        :param voxelDensity:
        :param MCSperDay: MC steps per Day. Default is 500, i.e. 500 MCS = 1 day.
        :param simDurationDays:
        :param fluctuationAmplitude:
        :param flip2DimRatio:
        :param neighborOrder:
        :param boundary_x:
        :param debugOutputFrequency:
        :param SEED:
        :return:
        """
        self.xLength = xLength
        self.yLength = yLength
        self.zLength = zLength
        self.voxelDensity = voxelDensity  # 1 voxel / 1 mu
        self.initNutrientDiffusion = initNutrientDiffusion
        self.dimensions = 2 if zLength <= 0 else 3
        self.xDimension = self.calcPixelFromMuMeter(xLength)
        self.yDimension = self.calcPixelFromMuMeter(yLength)
        self.zDimension = 1 if self.dimensions == 2 else self.calcPixelFromMuMeterMin1(zLength)
        self.latticeSizeInVoxel = self.xDimension * self.yDimension * self.zDimension
        self.MCSperDay = MCSperDay
        self.simDurationDays = simDurationDays
        self.sampleIntervalInDays = sampleIntervalInDays
        self.sampleIntervalInMCS = self.calcMCSfromDays(sampleIntervalInDays)
        self.maxSteps = self.calcMCSfromDays(simDurationDays)
        self.fluctuationAmplitude = fluctuationAmplitude
        self.flip2DimRatio = flip2DimRatio
        self.neighborOrder = neighborOrder
        self.boundary_x = boundary_x
        self.debugOutputFrequency = debugOutputFrequency
        # TODO: change the seed value of every random number used in Moduro project
        self.SEED = (int(round(time.time() * 1000)) % 9999) if SEED < 0 else SEED
        self.__cc3d = None
        self.parameterStore = ParameterStore()
        self.parameterStore.addObj(self)

    def initPotts(self):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Function ExecConfig.initPotts'

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
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Function ExecConfig.initCellTypes'

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
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Function ExecConfig.initEnergyMatrix'

        contact = self.__cc3d.ElementCC3D("Plugin", {"Name": "Contact"})
        for i in range(cellTypes.__len__()):
            for j in range(i, cellTypes.__len__()):
                print 'ExecConfig.initEnergyMatrix - i {} - J {} - VALUE {}'.format(i, j, adhFactor*energyMatrix[i][j])
                contact.ElementCC3D("Energy", {"Type1": cellTypes[i].name,
                                               "Type2": cellTypes[j].name},
                                    adhFactor * energyMatrix[i][j])

    def initPlugins(self, *args):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Function ExecConfig.initPlugins'

        for a in args:
            self.__cc3d.ElementCC3D("Plugin", {"Name": a})

    def initDiffusion(self, cellType, secretionRateNutr, decayConstantNutr):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Function ExecConfig.initDiffusion'

        SteppableElmnt = self.__cc3d.ElementCC3D("Steppable", {"Type": "FlexibleDiffusionSolverFE"})
        DiffusionFieldElmnt = SteppableElmnt.ElementCC3D("DiffusionField")
        DiffusionDataElmnt = DiffusionFieldElmnt.ElementCC3D("DiffusionData")
        DiffusionDataElmnt.ElementCC3D("FieldName", {}, "Nutrients")
        DiffusionDataElmnt.ElementCC3D("DiffusionConstant", {}, secretionRateNutr)
        DiffusionDataElmnt.ElementCC3D("DecayConstant", {}, decayConstantNutr)
        SecretionDataElmnt = DiffusionFieldElmnt.ElementCC3D("SecretionData")
        SecretionDataElmnt.ElementCC3D("Secretion", {"Type": cellType.name}, secretionRateNutr)

    def getCC3D(self):
        return self.__cc3d

    def calculateLatticeSize(self):
        return self.xDimension * self.yDimension * self.zDimension

        #cause the structure this function returns a boolean
    def interuptMCS(self, mcs): # see https://docs.python.org/release/2.7.3/library/stdtypes.html#boolean-operations-and-or-not
        return (mcs == 0) or (mcs % self.sampleIntervalInMCS == 0) # only evaluates the second argumend if the first is false

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
        #python has approximation errors when casted into int with long number of .99999999
        '''CC3D requires the amount of px in int.
        Therfore, check if float is larger .5 -> if so increase amount of px by 1
        It is still an approximation error, but better than just to cast the float to int'''

        #print'!!!!!!!!!!calcPixelFromMuMeter - param {} - voxelDensity {} - result {}'.format(mum, self.voxelDensity, self.voxelDensity*mum)
        pxInFloat = self.voxelDensity * mum
        #print'!!!!!!!!!!if mod 1 > 0.5 ----- px {} - px%1 {}'.format(pxInFloat, pxInFloat%1)
        if pxInFloat % 1.0 > 0.5:
            pxInFloat += 1

        return int(pxInFloat)
        #return int(self.voxelDensity * mum + 0.000001) # is __truncate(+0.000001) important?

    def calcPixelFromMuMeterMin1(self, mum):
        """
        Convert a length in micro meter to a pixel length.
        This is influenced by the voxelDensity.
        :param mum:
        :return:
        """
        return self.__truncate(self.voxelDensity * mum)

    def calculateVolume(self, diameter):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Function ExecConfig.calculateVolume'

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

        #def calcVoxelVolumeFromVolume(self, diameter):
        #amountPx = self.calcPixelFromMuMeter(diameter / 2)
        #print '!!!!!!!!calcVoxelVolumeFromVolume - diameter {} - amountPx {} - result {}'.format(diameter, amountPx, 4.0 / 3.0 * PI * (amountPx ** 3))
        #return 4.0 / 3.0 * PI * (amountPx ** 3)

        r = (3 * volume / (4.0 * PI)) ** (1.0 / 3.0)  # Radius of a sphere with known volume.

        #rDimension = self.calcPixelFromMuMeter(r)  # Convert it to a pixel unit.
        rDimension = r * self.voxelDensity
        if self.dimensions == 2:
            # a = self.__truncateToVoxel(PI * (rDimension ** 2))
            # if volume > 0:
            #    print "volume=", volume, ", rDim=", rDimension, ", r=", r, ", A=", a
            return int(self.__truncate(PI * (rDimension ** 2)))  # Area of a circle.
        else:
        #    print '!!!!!!!!!calcVoxelVolumeFromVolume(volume): result {}'.format(4.0 / 3.0 * PI * (rDimension ** 3))
            #print'rDimension {}'.format(rDimension)
            result = 4.0 / 3.0 * PI * (rDimension ** 3)
            if result % 1.0 > 0.5:
                result += 1

            return int(result)
            #return self.__truncate(4.0 / 3.0 * PI * (rDimension ** 3))  # Volume of a sphere.

    def calcVoxelSurfaceFromVoxelVolume(self, voxelVolume):
        """
        Calculates the voxel surface from a voxel volume. The results
        depends on the dimension of the simulation (2D or 3D).
        :param voxelVolume: volume (in pixel^3).
        :return: Surface in pixel^2 ^(3D) or pixel (2).
        """
        if self.dimensions == 2:
            # some fractal factor!
            return self.__truncate(1.5 * 2 * (PI * voxelVolume) ** (1.0 / 2.0))  # Circumference.
        else:
            return self.__truncate(2 * (4 * PI * (3 * voxelVolume / (4 * PI)) ** (2.0 / 3.0)))  # Surface.

    def __truncate(self, value):
        res = int(value + 0.00001)
        if res <= 1:
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

    def calcHoursFromMCS(self, mcs):
        """
        Convert the MCS number into hours.
        :param mcs:
        :return:
        """
        return mcs / (1.0 * self.MCSperDay) * 24.0
'''
    def calcSurLambdaFromSurFit(self, surFit):
        return 100.0 * surFit

    def calcVolLambdaFromVolFit(self, volFit):
        return 1.0 * volFit
'''