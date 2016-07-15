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

__author__ = "Julian Debatin"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "juliandebatin@gmail.com"
__status__ = "Production"


from Core.CellType import CellType
from Core.ExecConfig import ExecConfig
from Core.ModelConfig import ModelConfig
from Steppable.InitializerSteppable import InitializerSteppable
from Steppable.DeathSteppable import DeathSteppable
from Steppable.GrowthMitosisSteppable import GrowthMitosisSteppable
from Steppable.GrowthSteppable import GrowthSteppable
from Steppable.CMTransformationSteppable import CMTransformationSteppable
from Steppable.UrinationSteppable import UrinationSteppable
from Logger.VolumeFitnessSteppable import VolumeFitnessSteppable
from Logger.ArrangementFitnessSteppable import ArrangementFitnessSteppable
from Logger.DummyFitnessSteppable import DummyFitnessSteppable

class SdBpaIpaInUa(ModelConfig):
    def __init__(self, sim, simthread):
        ModelConfig.__init__(self, sim, simthread)

    def _initMOdel(self):
        self.name = "SdBpaIpaInUa"
        self.CellType = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self._run() # Must be the last statement.

    def _createCellTypes(self):
        cellTypes = []
        medium = CellType(name="Medium", frozen=True, minDiameter=0, maxDiameter=0,
                                growthVolumePerDay=0, nutrientRequirement=0, apoptosisTimeInDays=0,
                                volFit=1.0, surFit=1.0)

        basalmembrane = CellType(name="BasalMembrane", frozen=True, minDiameter=0, maxDiameter=0,
                                growthVolumePerDay=0, nutrientRequirement=0, apoptosisTimeInDays=180000,
                                volFit=1.0, surFit=1.0)

        stem = CellType(name="Stem", minDiameter=8, maxDiameter=10,
                                growthVolumePerDay=.010 * self.calcVolume(10),
                                nutrientRequirement=1.0, apoptosisTimeInDays=180000,
                                volFit=1, surFit=0.5)

        basal = CellType(name="Basal", minDiameter=9, maxDiameter=10,
                                growthVolumePerDay=0.12 * self.calcVolume(10),
                                nutrientRequirement=1.0, apoptosisTimeInDays=80,
                                volFit=0.9, surFit=0.5)

        intermediate = CellType(name="Intermediate", minDiameter=12, maxDiameter=15,
                                growthVolumePerDay=0.04 * self.calcVolume(15),
                                nutrientRequirement=1.0, apoptosisTimeInDays=20,
                                volFit=0.9, surFit=0.1)

        umbrella = CellType(name="Umbrella", minDiameter=15, maxDiameter=19,
                                growthVolumePerDay=0.01 * self.calcVolume(19),
                                nutrientRequirement=1.0, apoptosisTimeInDays=10,
                                volFit=0.9, surFit=0.1)

        stem.setDescendants(1.0, [stem.id, basal.id])
        basal.setDescendants(0.9, [basal.id, intermediate.id])
        basal.setDescendants(0.05, [basal.id, basal.id])
        basal.setDescendants(0.05, [intermediate.id, intermediate.id])
        intermediate.setDescendants(0.98, [intermediate.id, umbrella.id])
        intermediate.setDescendants(0.01, [intermediate.id, intermediate.id])
        intermediate.setDescendants(0.01, [umbrella.id, umbrella.id])

        cellTypes.extend((medium, basalmembrane, stem, basal, intermediate, umbrella))

        return cellTypes

    def _getSteppables(self):
        steppableList = []
        steppableList.append(InitializerSteppable(self.sim, self))
        steppableList.append(GrowthSteppable(self.sim, self))
        steppableList.append(GrowthMitosisSteppable(self.sim, self))
        steppableList.append(CMTransformationSteppable(self.sim, self))
        steppableList.append(UrinationSteppable(self.sim, self, prop=0.02))
        steppableList.append(DeathSteppable(self.sim, self))
        # steppableList.append(OptimumSearchSteppable(self.sim, self))
        steppableList.append(VolumeFitnessSteppable(self.sim, self))
        steppableList.append(ArrangementFitnessSteppable(self.sim, self))
        steppableList.append(DummyFitnessSteppable(self.sim, self))

        return steppableList

    def _createExecConfig(self):
        return ExecConfig(MCSperDay=500, SEED=10,
                          xLength=500, yLength=150, zLength=0, voxelDensity=.8)
