from Core.CellType import CellType
from Core.ExecConfig import ExecConfig
from Core.ModelConfig import ModelConfig
from Steppable.ConstraintInitializerSteppable import ConstraintInitializerSteppable
from Steppable.DeathSteppable import DeathSteppable
from Steppable.GrowthMitosisSteppable import GrowthMitosisSteppable
from Steppable.GrowthSteppable import GrowthSteppable
from Steppable.OptimumSearchSteppable import OptimumSearchSteppable
from Steppable.TransformationSteppable import TransformationSteppable
from Steppable.UrinationSteppable import UrinationSteppable
from ModuroModel.CMInDae import CMInDae


class PASCMInDae(CMInDae):
    def __init__(self, sim, simthread):
        ModelConfig.__init__(self, sim, simthread)

    def run(self, srcDir):
        self.name = "PASCM"
        super(PASCMInDae, self).run(srcDir)  # TODO could be in constructor?!
        # Example for setting a parameter.
        self.execConfig.parameterStore.setParameter("PASCMInDae", "dae", True)

    def _createCellTypes(self):
        cellTypes = []
        cellTypes.append(CellType(name="Medium", frozen=True, minDiameter=0, maxDiameter=0,
                                  growthVolumePerDay=0, nutrientRequirement=0, apoptosisTimeInDays=0,
                                  volFit=0.9, surFit=1.0, differentiates=False, asym=0.0))

        cellTypes.append(CellType(name="BasalMembrane", frozen=True, minDiameter=0, maxDiameter=0,
                                  growthVolumePerDay=0, nutrientRequirement=0, apoptosisTimeInDays=180000,
                                  volFit=0.9, surFit=0.1, differentiates=False, asym=0.0))

        cellTypes.append(CellType(name="Stem", minDiameter=8, maxDiameter=10,
                                  growthVolumePerDay=10 * self.calcVolume(10),
                                  nutrientRequirement=1.0, apoptosisTimeInDays=180000,
                                  volFit=0.9, surFit=0.1, differentiates=False,
                                  asym=0.90, idenSym=0.05, diffSym=0.05))

        cellTypes.append(CellType(name="Basal", minDiameter=10, maxDiameter=12,
                                  growthVolumePerDay=10 * self.calcVolume(12),
                                  nutrientRequirement=1.0, apoptosisTimeInDays=90,
                                  volFit=0.9, surFit=0.1, differentiates=True))

        cellTypes.append(CellType(name="Intermediate", minDiameter=12, maxDiameter=15,
                                  growthVolumePerDay=10 * self.calcVolume(15),
                                  nutrientRequirement=1.0, apoptosisTimeInDays=90,
                                  volFit=0.9, surFit=0.1, differentiates=True))

        cellTypes.append(CellType(name="Umbrella", minDiameter=15, maxDiameter=19,
                                  growthVolumePerDay=10 * self.calcVolume(19),
                                  nutrientRequirement=1.0, apoptosisTimeInDays=90,
                                  volFit=0.9, surFit=0.1, differentiates=True))

        return cellTypes

    def _createExecConfig(self, srcDir):
        return ExecConfig(srcDir=srcDir,
                          xLength=200, yLength=100, zLength=50, voxelDensity=0.8,
                          MCSperDay=500,
                          SEED=123)