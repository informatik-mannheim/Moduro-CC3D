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


from Core.CellType import *
from Core.ExecConfig import ExecConfig
from Core.ModelConfig import ModelConfig
from Steppable.InitializerSteppable import InitializerSteppable
from Steppable.DeathSteppable import DeathSteppable
from Steppable.GrowthMitosisSteppable import GrowthMitosisSteppable
from Steppable.GrowthSteppable import GrowthSteppable
from Steppable.IntermediateTransformationSteppable import IntermediateTransformationSteppable
from Steppable.CMTransformationSteppable import CMTransformationSteppable
from Steppable.UrinationSteppable import UrinationSteppable
from Logger.VolumeFitnessSteppable import VolumeFitnessSteppable
from Logger.ArrangementFitnessSteppable import ArrangementFitnessSteppable
from Logger.DummyFitnessSteppable import DummyFitnessSteppable
from Steppable.ColonySteppable import ColonySteppable
from Steppable.MutationSteppable import MutationSteppable

class SdBpaCdiInUa(ModelConfig):
    def __init__(self, sim, simthread):
        ModelConfig.__init__(self, sim, simthread)

    def _initModel(self):
        self.name = "SdBpaCdiInUa"
        self.CellType = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self._run() # Must be the last statement.

    def _createCellTypes(self):
        cellTypes = []
        stem = Stemcell
        stem.setGrowthVolumePerDayRelVolume(0.13)
        #stem.apoptosisTimeInDays = 60.0
        self.necrosisProbStem = stem.necrosisProb = 0.0

        basal = Basalcell
        basal.setGrowthVolumePerDayRelVolume(0.12)
        basal.apoptosisTimeInDays = 180000.0
        self.necrosisProbBasal = basal.necrosisProb = 0.000008

        intermediate = Intermediatecell
        intermediate.setGrowthVolumePerDayRelVolume(0.11)
        intermediate.apoptosisTimeInDays = 180000.0
        self.necrosisProbIntermediate = intermediate.necrosisProb = 0.00003

        umbrella = Umbrellacell
        umbrella.setGrowthVolumePerDayRelVolume(0.1)
        umbrella.apoptosisTimeInDays = 180000.0
        self.necrosisProbUmbrella = umbrella.necrosisProb = 0.000035

        stem.setDescendants(1.0, [stem.id, basal.id])
        basal.setDescendants(0.96, [basal.id, intermediate.id])
        basal.setDescendants(0.02, [basal.id, basal.id])
        basal.setDescendants(0.02, [intermediate.id, intermediate.id])


        cellTypes.extend((Medium, Basalmembrane, stem, basal, intermediate, umbrella))

        return cellTypes

    def _getSteppables(self):
        steppableList = []
        steppableList.append(ColonySteppable(self.sim, self))
        steppableList.append(InitializerSteppable(self.sim, self))
        steppableList.append(GrowthSteppable(self.sim, self))
        steppableList.append(GrowthMitosisSteppable(self.sim, self))
        steppableList.append(IntermediateTransformationSteppable(self.sim, self))
        #steppableList.append(CMTransformationSteppable(self.sim, self))
        steppableList.append(UrinationSteppable(self.sim, self, prop=0.02))
        steppableList.append(DeathSteppable(self.sim, self))
        # steppableList.append(OptimumSearchSteppable(self.sim, self))
        steppableList.append(VolumeFitnessSteppable(self.sim, self))
        steppableList.append(ArrangementFitnessSteppable(self.sim, self))
        steppableList.append(DummyFitnessSteppable(self.sim, self))
        steppableList.append(MutationSteppable(self.sim, self, self.necrosisProbStem, self.necrosisProbBasal,
                                               self.necrosisProbIntermediate, self.necrosisProbUmbrella))

        return steppableList

    def _createExecConfig(self):
        return ExecConfig(MCSperDay=500,  # SEED=10,
                          xLength=500, yLength=150, zLength=100, voxelDensity=.5)
