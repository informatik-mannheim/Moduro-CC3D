import sys

from Core.ExecConfig import ExecConfig
from Core.ModelConfig import ModelConfig
from Core.CellType import *
from Logger.ArrangementFitnessSteppable import ArrangementFitnessSteppable
from Logger.DummyFitnessSteppable import DummyFitnessSteppable
from Logger.VolumeFitnessSteppable import VolumeFitnessSteppable
from Steppable.CMTransformationSteppable import CMTransformationSteppable
from Steppable.ColonySteppable import ColonySteppable
from Steppable.DeathSteppable import DeathSteppable
from Steppable.GrowthMitosisSteppable import GrowthMitosisSteppable
from Steppable.GrowthSteppable import GrowthSteppable
from Steppable.InitializerSteppable import InitializerSteppable
from Steppable.MutationSteppable import MutationSteppable
from Steppable.UrinationSteppable import UrinationSteppable


class JsonBasedModelUa(ModelConfig):
    def __init__(self, sim, simthread):
        ModelConfig.__init__(self, sim, simthread)

    def _initModel(self):
        self.name = "JsonBasedModelUa"
        self.CellType = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self._run()  # Must be the last statement.

    def createCellTypesByJson(self, parsedJson):
        parsedJsonCellTypes = parsedJson['parameterDumpCellTypeList']
        celltypes = []

        # CellType Medium and CellType Basalmembrane are not optimizable and therefore we use the default values
        celltypes.append(Medium)  # has to have ID: 0
        celltypes.append(Basalmembrane)  # has to have ID: 1

        # The following 4 celltypes are affected by value optimization by Moduro-Toolbox
        aStemCell = self.createCellTypeStem(parsedJsonCellTypes)
        aBasalCell = self.createCellTypeBasal(parsedJsonCellTypes)
        aIntermediateCell = self.createCellTypeIntermediate(parsedJsonCellTypes)
        aUmbrellaCell = self.createCellTypeUmbrella(parsedJsonCellTypes)

        # necrosis prob values
        self.intermediateNecrosisProb = aIntermediateCell.necrosisProb
        self.stemNecrosisProb = aStemCell.necrosisProb
        self.basalNecrosisProb = aBasalCell.necrosisProb
        self.umbrellaNecrosisProb = aUmbrellaCell.necrosisProb

        celltypes.append(aStemCell)
        celltypes.append(aBasalCell)
        celltypes.append(aIntermediateCell)
        celltypes.append(aUmbrellaCell)

        return celltypes

    def createCellTypeStem(self, parsedStemCellTypes):
        # cellStemgrowthVolumePerDay depends on the value of Math.calcSphereVolumeFromDiameter(self.maxDiameter)
        # A JSON import requires the file has been imported from ParameterDump.dat in Moduro Toolbox before.
        # This means the Relative Volume has been calculated in respect of the maxDiamaeter, before the value was set
        # in the origin ParameterDump.dat.
        # So we will just set the value of growthVolumePerDay directly for all CellTypes
        # The settermethod to calculate the relativeVolume is: setGrowthVolumePerDayRelVolume
        return self.setCellTypeParameters(Stemcell, "Stem", parsedStemCellTypes)

    def createCellTypeBasal(self, parsedStemCellTypes):
        return self.setCellTypeParameters(Basalcell, "Basal", parsedStemCellTypes)

    def createCellTypeIntermediate(self, parsedStemCellTypes):
        return self.setCellTypeParameters(Intermediatecell, "Intermediate", parsedStemCellTypes)

    def createCellTypeUmbrella(self, parsedStemCellTypes):
        return self.setCellTypeParameters(Umbrellacell, "Umbrella", parsedStemCellTypes)

    def _getSteppables(self):
        steppableList = []
        steppableList.append(ColonySteppable(self.sim, self))
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
        steppableList.append(MutationSteppable(self.sim, self, self.stemNecrosisProb, self.basalNecrosisProb,
                                               self.intermediateNecrosisProb, self.umbrellaNecrosisProb))

        return steppableList

    def setCellTypeParameters(self, cellTypeTarget, cellTypeJsonName, parsedStemCellTypes):
        jsonCellTypeValues = [cellType for cellType in parsedStemCellTypes if (cellType['name'] == cellTypeJsonName)]
        if len(jsonCellTypeValues) != 1:
            sys.exit(
                'error, invalid JSON values detected. There has to be exactly CellType defined with name: Intermediate')

        jsonCellTypeValues = jsonCellTypeValues[0]
        cellTypeTarget.apoptosisTimeInDays = jsonCellTypeValues['apoptosisTimeInDays']
        cellTypeTarget.consumPerCell = jsonCellTypeValues['consumPerCell']

        for descendantSet in jsonCellTypeValues['descendantsList']:
            cellTypeTarget.setDescendants(descendantSet['probability'],
                                          [descendantSet['cellId1'], descendantSet['cellId2']])

        cellTypeTarget.divides = jsonCellTypeValues['divides']
        cellTypeTarget.frozen = jsonCellTypeValues['frozen']

        # Already relative value
        # There is a method setGrothVolumePerDay which calculates the volume in respect of the maxDiameter
        # Since the JSON is based on an existing ParameterDump file, the value for growthVolumePerDay has been
        # calculated already. So we will not call the method to set the grothVolumePerDay but set it directly
        cellTypeTarget.growthVolumePerDay = jsonCellTypeValues['growthVolumePerDay']

        cellTypeTarget.id = jsonCellTypeValues['id']
        cellTypeTarget.maxDiameter = jsonCellTypeValues['maxDiameter']
        cellTypeTarget.minDiameter = jsonCellTypeValues['minDiameter']
        cellTypeTarget.minVol = jsonCellTypeValues['minVol']
        cellTypeTarget.necrosisProb = jsonCellTypeValues['necrosisProb']
        cellTypeTarget.nutrientRequirement = jsonCellTypeValues['nutrientRequirement']
        cellTypeTarget.surFit = jsonCellTypeValues['surFit']
        cellTypeTarget.volFit = jsonCellTypeValues['volFit']

        return cellTypeTarget

    def _createExecConfig(self):
        return ExecConfig(MCSperDay=500,  # SEED=10,
                          xLength=500, yLength=150, zLength=0, voxelDensity=.8)