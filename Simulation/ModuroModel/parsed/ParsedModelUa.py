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

__author__ = "Karin Adler"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "karin.adler@stud.hs-mannheim.de"
# todo: update state before merging with master
__status__ = "Developemt 05.12.2016"

from Core.CellType import *
from Core.ExecConfig import ExecConfig
from Core.ModelConfig import ModelConfig
from ParameterDatToObjectConverter import ParameterDumpToObjectsConverter

from Steppable.InitializerSteppable import InitializerSteppable
from Steppable.DeathSteppable import DeathSteppable
from Steppable.GrowthMitosisSteppable import GrowthMitosisSteppable
from Steppable.GrowthSteppable import GrowthSteppable
from Steppable.CMTransformationSteppable import CMTransformationSteppable
from Steppable.UrinationSteppable import UrinationSteppable
from Logger.VolumeFitnessSteppable import VolumeFitnessSteppable
from Logger.ArrangementFitnessSteppable import ArrangementFitnessSteppable
from Logger.DummyFitnessSteppable import DummyFitnessSteppable
from Steppable.ColonySteppable import ColonySteppable
from Steppable.MutationSteppable import MutationSteppable


class ParsedModelUa(ModelConfig):
    def __init__(self, sim, simthread, parameter_dump_path):
            self.parameterDumpPath = parameter_dump_path
            ModelConfig.__init__(self, sim, simthread)

    def _initModel(self):
            paramDumpConverter = ParameterDumpToObjectsConverter()
            #todo: name klären (1zu1 aus parameterDump? Oder mit Präfix? Suffix?)
            # self.name = "parsedModel"
            self.name = paramDumpConverter.getNameOfModel(self.parameterDumpPath)
            self.cellTypes = self._createCellTypes()
            self.energyMatrix = self._createEnergyMatrix()
            self._run()  # Must be the last statement.

    def _createCellTypes(self):
                #pramDumpConverter = ParameterDumpToObjectsConverter()

                cellTypes = []
                stem = Stemcell
                stem.setGrowthVolumePerDayRelVolume()

                # todo: wird das verwendet?
                self.stemNecrosisProb = stem.necrosisProb = 0

               # todo: WIRD DURCH DEN PARAMETERDATTOOBJECTCONV ausgetauscht!!!
               # stemCell = paramDumpConverter.getStemCell(self.parameterDumpPath)
               # basalCell = paramDumpConverter.getBasalcell(self.parameterDumpPath)
               # umbrellaCell = paramDumpConverter.getUmbrellacell(self.parameterDumpPath)
               # basalMembrane = paramDumpConverter.getBasalmembrane(self.parameterDumpPath)
               # ...

                basal = Basalcell
                basal.setGrowthVolumePerDayRelVolume(0.12)
                basal.apoptosisTimeInDays = 8000000000.0
                self.basalNecrosisProb = basal.necrosisProb = 0.00001

                intermediate = Intermediatecell
                intermediate.setGrowthVolumePerDayRelVolume(0.11)
                intermediate.apoptosisTimeInDays = 20000000000.0
                self.intermediateNecrosisProb = intermediate.necrosisProb = 0.00003

                umbrella = Umbrellacell
                umbrella.setGrowthVolumePerDayRelVolume(0.09)
                umbrella.apoptosisTimeInDays = 100000000000.0
                self.umbrellaNecrosisProb = umbrella.necrosisProb = 0.00005

                # todo kann nicht im converter gesetzt werden
                # todo: auf reihenfolge beim Anlegen der Klassen achten!
                # CellType setzt ID lokal (counter im konstruktor)
                stem.setDescendants(0.90, [stem.id, basal.id])
                stem.setDescendants(0.05, [stem.id, stem.id])
                stem.setDescendants(0.05, [basal.id, basal.id])
                basal.setDescendants(1.0, [basal.id, intermediate.id])

                cellTypes.extend((Medium, Basalmembrane, stem, basal, intermediate, umbrella))

                return cellTypes
