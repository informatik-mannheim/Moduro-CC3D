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

from Logger.TissueFitnessSteppable import TissueFitnessSteppable


class VolumeFitnessSteppable(TissueFitnessSteppable):
    def __init__(self, simulator, model, _frequency=1):
        TissueFitnessSteppable.__init__(self, simulator, model, "FitnessVolume.dat", _frequency)
        yDim = self.execConfig.calcPixelFromMuMeterMin1(85)
        self.idealVol = self.execConfig.xDimension * yDim * self.execConfig.zDimension
        self.idealBasalStemCellsVol = 0.10 * self.idealVol
        self.idealIntermediateCellsVol = 0.67 * self.idealVol
        self.idealUmbrellaCellsVol = 0.23 * self.idealVol

    # step is overwritten
    def step(self, mcs):
        if self.execConfig.interuptMCS(mcs):
            totalVolume = 0
            umbrellaVolume = 0
            intermediateVolume = 0
            basalStemVolume = 0
            mediumVolume = self.latticeSize
            for cell in self.cellList:
                if cell.type == self.BASALMEMBRANE:
                    mediumVolume -= cell.volume
                if cell.type > self.BASALMEMBRANE:
                    totalVolume += cell.volume
                    if cell.type == self.UMBRELLA:
                        umbrellaVolume += cell.volume
                        mediumVolume -= cell.volume
                    elif cell.type == self.INTERMEDIATE:
                        intermediateVolume += cell.volume
                        mediumVolume -= cell.volume
                    else:
                        basalStemVolume += cell.volume
                        mediumVolume -= cell.volume
            if totalVolume == 0 or mediumVolume == 0:
                fitness_v = 0.0
                # print "No more cell in simulation"
                self.stopSimulation()
            else:

                fitness_B = self._fit(self.idealBasalStemCellsVol, basalStemVolume)
                fitness_I = self._fit(self.idealIntermediateCellsVol, intermediateVolume)
                fitness_U = self._fit(self.idealUmbrellaCellsVol, umbrellaVolume)

                fitness_v = (fitness_B + fitness_I + fitness_U) / 3.0
                # print "!R!R!R!R!RR! lattice=", self.latticeSize, ", idealL=", self.idealVol, ", tVoxel=", totalVolume
                # print "!!!!!! B ", self.idealBasalStemCellsVol, " = ", basalStemVolume
                # print "!!!!!! I ", self.idealIntermediateCellsVol, " = ", intermediateVolume
                # print "!!!!!! U ", self.idealUmbrellaCellsVol, " = ", umbrellaVolume
                # print "!!!!!! fB = ", fitness_B,", fI = ", fitness_I,", fU = ", fitness_U

            self._addLine(mcs, fitness_v, fitness_B, fitness_I, fitness_U)

    def _fit(self, volOpt, vol):
        return 1.0 / (4.0 * ((volOpt - vol) / volOpt) ** 2.0 + 1.0)
