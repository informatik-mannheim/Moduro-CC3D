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
from math import pi as PI, sqrt
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
                 fluctuationAmplitude=1.0,  #temperature in simulation
                 flip2DimRatio=0.5,
                 neighborOrder=6,   #was 1 -> tip of allanswered topic
                 boundary_x="Periodic",
                 debugOutputFrequency=50000,
                 SEED=-1):
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
        self.zDimension = 1 if self.dimensions == 2 else self.calcPixelFromMuMeter(zLength)
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
        '''CC3D requires the amount of px in int.
        Therfore, check if float is larger .5 -> if so increase amount of px by 1
        It is still an approximation error, but better than just to cast the float to int'''

        pxInFloat = self.voxelDensity * mum

        if pxInFloat % 1.0 > 0.5:
            pxInFloat += 1


        return int(pxInFloat)
        #return int(self.voxelDensity * mum + 0.000001) # is __truncate(+0.000001) important?

    def calcFloatPixel(self, mum):
        if self.voxelDensity == 1:
            return mum
        else:
            return float(self.voxelDensity * mum)

    def calcPixelFromMuMeterMin1(self, mum):
        """
        Convert a length in micro meter to a pixel length.
        This is influenced by the voxelDensity.
        :param mum:
        :return:
        """
        return self.__truncate(self.voxelDensity * mum)


    def calcVoxelVolumeFromVolume(self, volume):
        """
        Calculates the voxel volume from a physical volume. The results
        depends on the dimension of the simulation (2D or 3D).
        The scaling is influenced by the voxelDensity.
        :param volume: physical volume in mu m^3.
        :return: Voxel volume.
        """
        r = (3 * volume / (4.0 * PI)) ** (1.0 / 3.0)  # Radius of a sphere with known volume.

        rDimension = r * self.voxelDensity
        if self.dimensions == 2:
            return int(self.__truncate(PI * (rDimension ** 2)))  # Area of a circle.
        else:
            result = 4.0 / 3.0 * PI * (rDimension ** 3)
            if result % 1.0 >= 0.5:
                result += 1
            return int(result)

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
            return self.__truncate(1.5 * (4 * PI * (3 * voxelVolume / (4 * PI)) ** (2.0 / 3.0)))  # Surface.

    def __truncate(self, value):
        res = int(value + 0.00001)
        if res <= 1:
            return 1  # Ensure that size is at least 1.
        else:
            return res


    def calcPixelSphereSurface(self, volume):
        if volume != 0:
            radius = (3 * volume / (4.0 * PI)) ** (1.0 / 3.0)  # Radius of a sphere with known volume.
            diameter = 2 * radius
            if radius % 1 >= 0.5:
                radius = int(radius+1)
            amountPixel = int(2*radius)
            pixelDistance = float(diameter)/float(amountPixel)
            Matrix = [[[1 for x in range(0, amountPixel / 2)] for z in range(0, amountPixel / 2)] for y in
                      range(0, amountPixel / 2)]
            PixelsInSphere = 0
            VolumeOfVoxel = pixelDistance ** 3
            SurfaceVoxelSite = pixelDistance ** 2

            # set pixels in the matrix
            for k in xrange(0, amountPixel / 2):
                if k == amountPixel / 2:
                    x1 = 0
                else:
                    x1 = k
                x2 = x1 + pixelDistance
                for l in xrange(0, amountPixel / 2):
                    if l == amountPixel / 2:
                        z1 = 0
                    else:
                        z1 = l
                    z2 = z1 + pixelDistance

                    xzPoint = radius ** 2 - (x1 + ((x2 - x1) / 2.)) ** 2 - (z1 + ((z2 - z1) / 2.)) ** 2
                    if xzPoint <= 0:
                        yr = 0
                    else:
                        yr = sqrt(xzPoint)
                    centerOfPixel = pixelDistance / 2.

                    for m in xrange(0, amountPixel / 2):
                        if centerOfPixel <= yr:
                            Matrix[k][l][m] = 0
                        centerOfPixel += pixelDistance

            # count the voxel of the pixel sphere
            for x in xrange(0, amountPixel / 2):
                for z in xrange(0, amountPixel / 2):
                    for y in xrange(0, amountPixel / 2):
                        if Matrix[x][z][y] == 0:
                            PixelsInSphere += 1

            # count the surface sites of the voxels at the surface
            pixelSurface = 0
            for x in xrange(0, amountPixel / 2):
                for z in xrange(0, amountPixel / 2):
                    for y in xrange(0, amountPixel / 2):
                        if Matrix[x][z][y] == 0:
                            if y + 1 >= amountPixel / 2 or Matrix[x][z][y + 1] == 1:
                                pixelSurface += 1

                            if x + 1 >= amountPixel / 2 or Matrix[x + 1][z][y] == 1:
                                pixelSurface += 1

                            if z + 1 >= amountPixel / 2 or Matrix[x][z + 1][y] == 1:
                                pixelSurface += 1

            return [int((((PixelsInSphere*2)*2)*2) * VolumeOfVoxel),
                    int((((pixelSurface*2)*2)*2) * SurfaceVoxelSite)]
        else:
            return [1, 1]

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
