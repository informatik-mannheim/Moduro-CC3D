from Core.CellType import CellType
from Core.ExecConfig import ExecConfig
from Core.ModelConfig import ModelConfig
from Steppable.ConstraintInitializerSteppable import ConstraintInitializerSteppable
from Steppable.DeathSteppable import DeathSteppable
from Steppable.GrowthMitosisSteppable import GrowthMitosisSteppable
from Steppable.GrowthSteppable import GrowthSteppable
from Steppable.TransformationSteppable import TransformationSteppable
from Steppable.UrinationSteppable import UrinationSteppable
from Logger.VolumeFitnessSteppable import VolumeFitnessSteppable
from Logger.ArrangementFitnessSteppable import ArrangementFitnessSteppable
from Logger.DummyFitnessSteppable import DummyFitnessSteppable


class CMInUa(ModelConfig):
    def __init__(self, sim, simthread, srcDir):
        ModelConfig.__init__(self, sim, simthread, srcDir)

    def _initModel(self):
        self.name = "CMInUa"
        self.adhFactor = 0.5  # average adhesion = 0.5
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self.execConfig.parameterStore.setParameter("CMInUa", "dae", True)
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
                                  growthVolumePerDay=10 * self.calcVolume(10),
                                  nutrientRequirement=1.0, apoptosisTimeInDays=180000,
                                  volFit=0.9, surFit=0.5, divides=True)

        basal = CellType(name="Basal", minDiameter=10, maxDiameter=12,
                                  growthVolumePerDay=10 * self.calcVolume(12),
                                  nutrientRequirement=1.0, apoptosisTimeInDays=90,
                                  volFit=0.9, surFit=0.5, divides=False, transforms=True)

        intermediate = CellType(name="Intermediate", minDiameter=12, maxDiameter=15,
                                  growthVolumePerDay=20 * self.calcVolume(15),
                                  nutrientRequirement=1.0, apoptosisTimeInDays=30,
                                  volFit=0.9, surFit=0.1, divides=False, transforms=True)

        umbrella = CellType(name="Umbrella", minDiameter=15, maxDiameter=19,
                                  growthVolumePerDay=10 * self.calcVolume(19),
                                  nutrientRequirement=1.0, apoptosisTimeInDays=10,
                                  volFit=0.9, surFit=0.1)

        stem.setDescendants(1.0, [stem, basal])
        basal.setDescendants(1.0, [intermediate])
        intermediate.setDescendants(1.0, [umbrella])

        cellTypes.extend((medium, basalmembrane, stem, basal, intermediate, umbrella))

        return cellTypes

    def _getSteppables(self):
        steppableList = []
        steppableList.append(ConstraintInitializerSteppable(self.sim, self))
        steppableList.append(GrowthSteppable(self.sim, self))
        steppableList.append(GrowthMitosisSteppable(self.sim, self))
        steppableList.append(TransformationSteppable(self.sim, self))
        steppableList.append(UrinationSteppable(self.sim, self, prop=0.02))
        steppableList.append(DeathSteppable(self.sim, self))
        #steppableList.append(OptimumSearchSteppable(self.sim, self))
        steppableList.append(VolumeFitnessSteppable(self.sim, self))
        steppableList.append(ArrangementFitnessSteppable(self.sim, self))
        steppableList.append(DummyFitnessSteppable(self.sim, self))

        return steppableList

    def _createExecConfig(self, srcDir):
        return ExecConfig(srcDir=srcDir,
                          xLength=150, yLength=100, zLength=0, voxelDensity=1)
