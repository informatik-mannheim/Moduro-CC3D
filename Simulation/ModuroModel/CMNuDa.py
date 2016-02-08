from Core.CellType import CellType
from Core.ExecConfig import ExecConfig
from Core.ModelConfig import ModelConfig
from Steppable.ConstraintInitializerSteppable import ConstraintInitializerSteppable
from Steppable.DeathSteppable import DeathSteppable
from Steppable.GrowthMitosisSteppable import GrowthMitosisSteppable
from Steppable.NutrientGrowthSteppable import NutrientGrowthSteppable
from Steppable.OptimumSearchSteppable import OptimumSearchSteppable
from Steppable.TransformationSteppable import TransformationSteppable
from Steppable.UrinationSteppable import UrinationSteppable


class CMNuDa(ModelConfig):
    def __init__(self, sim, simthread):
        ModelConfig.__init__(self, sim, simthread)
        self.name = "CMNuDa"
        self._nutrient = True
        self._dae = True
        # Must be invoked again as _dae has changed:
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix(1.0)

    def _createCellTypes(self):
        cellTypes = []
        medium = CellType(name="Medium", frozen=True, minDiameter=0, maxDiameter=0, growthVolumePerDay=0,
                          nutrientRequirement=0, apoptosisTimeInDays=0,
                          volFit=1.0, surFit=1.0, differentiates=False, asym=0.0)
        basalmembrane = CellType(name="BasalMembrane", frozen=True, minDiameter=0, maxDiameter=0, growthVolumePerDay=0,
                                 nutrientRequirement=0, apoptosisTimeInDays=180000,
                                 volFit=1.0, surFit=1.0, differentiates=False, asym=0.0)
        stem = CellType("Stem", False, 10, 10, 0.02, 1.0, 180000, 1.0, 0.0, True, 1.0)
        basal = CellType("Basal", False, 11, 12, 0.02, 1.0, 90, 1.0, 0.0, True, 0.0)
        intermediate = CellType("Intermediate", False, 15, 18, 0.04, 1.0, 30, 10.0, 1.0, True, 0.0)
        umbrella = CellType("Umbrella", False, 22, 24, 0.08, 1.0, 10, 10.0, 1.0, False, 0.0)

        cellTypes.append(medium)
        cellTypes.append(basalmembrane)
        cellTypes.append(stem)
        cellTypes.append(basal)
        cellTypes.append(intermediate)
        cellTypes.append(umbrella)

        return cellTypes


    def _createEnergyMatrix(self, adhFac=1.0):
        energyMatrix = [[1 * adhFac for x in range(self.cellTypes.__len__())]
                        for x in range(self.cellTypes.__len__())]

        if self.withDAE():
            energyMatrix = [[adhFac * 0, adhFac * 14, adhFac * 14, adhFac * 14, adhFac * 14, adhFac * 4],
                            [0, adhFac * -1, adhFac * 1, adhFac * 3, adhFac * 12, adhFac * 12],
                            [0, 0, adhFac * 6, adhFac * 4, adhFac * 8, adhFac * 14],
                            [0, 0, 0, adhFac * 5, adhFac * 8, adhFac * 12],
                            [0, 0, 0, 0, adhFac * 6, adhFac * 4],
                            [0, 0, 0, 0, 0, adhFac * 2]]

        return energyMatrix


    def withNutrient(self):
        return self._nutrient

    def withDAE(self):
        return self._dae


    def _getSteppables(self):
        steppableList = []
        steppableList.append(ConstraintInitializerSteppable(self.sim, self.execConfig, self))
        steppableList.append(NutrientGrowthSteppable(self.sim, self.execConfig, self))
        steppableList.append(GrowthMitosisSteppable(self.sim, self.execConfig, self))
        steppableList.append(TransformationSteppable(self.sim, self.execConfig, self))
        steppableList.append(UrinationSteppable(self.sim, self.execConfig, self))
        steppableList.append(DeathSteppable(self.sim, self.execConfig, self))
        steppableList.append(OptimumSearchSteppable(self.sim, self.execConfig, self))

        return steppableList

    def _createExecConfig(self, srcDir):
        return ExecConfig(srcDir, xLength=150, yLength=200, zLength=1)
