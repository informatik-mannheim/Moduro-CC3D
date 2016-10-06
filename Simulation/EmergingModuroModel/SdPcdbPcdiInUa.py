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

from Core.CellType import *
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


class SdPcdbPcdiInUa(ModelConfig):
    def __init__(self, sim, simthread):
        ModelConfig.__init__(self, sim, simthread)

    def _initModel(self):
        self.name = "SdPcdbPcdiInUa"
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self._run()  # Must be the last statement.

    def _createCellTypes(self):
        cellTypes = []

        stem = Stemcell
        stem.setGrowthVolumePerDayRelVolume(0.010)

        basal = Basalcell
        basal.setGrowthVolumePerDayRelVolume(0.015)
        basal.apoptosisTimeInDays = 70.0 # actually not used.

        intermediate = Intermediatecell
        intermediate.setGrowthVolumePerDayRelVolume(0.012)
        intermediate.apoptosisTimeInDays = 70.0

        umbrella = Umbrellacell
        umbrella.setGrowthVolumePerDayRelVolume(0.012)
        umbrella.apoptosisTimeInDays = 70.0

        stem.setDescendants(1.0, [stem.id, basal.id])
        basal.setDescendants(1.0, [basal.id, basal.id])
        intermediate.setDescendants(1.0, [intermediate.id, intermediate.id])

        cellTypes.extend((Medium, Basalmembrane, stem, basal, intermediate, umbrella))

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
        return ExecConfig(xLength=800, yLength=150, zLength=0, voxelDensity=0.8,
                          MCSperDay=500)