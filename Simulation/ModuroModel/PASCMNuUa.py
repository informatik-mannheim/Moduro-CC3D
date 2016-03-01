from Core.CellType import CellType
from Core.ExecConfig import ExecConfig
from ModuroModel.CMNuUa import CMNuUa


class PASCMNuUa(CMNuUa):
    def __init__(self, sim, simthread, srcDir):
        CMNuUa.__init__(self, sim, simthread, srcDir)

    def _initModel(self):
        self.name = "PASCMNuUa"
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self._run()  # Must be the last statement.

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
                                  volFit=0.9, surFit=0.5)

        basal = CellType(name="Basal", minDiameter=10, maxDiameter=12,
                                  growthVolumePerDay=10 * self.calcVolume(12),
                                  nutrientRequirement=1.0, apoptosisTimeInDays=90,
                                  volFit=0.9, surFit=0.5)

        intermediate = CellType(name="Intermediate", minDiameter=12, maxDiameter=15,
                                  growthVolumePerDay=20 * self.calcVolume(15),
                                  nutrientRequirement=1.0, apoptosisTimeInDays=30,
                                  volFit=0.9, surFit=0.1)

        umbrella = CellType(name="Umbrella", minDiameter=15, maxDiameter=19,
                                  growthVolumePerDay=10 * self.calcVolume(19),
                                  nutrientRequirement=1.0, apoptosisTimeInDays=10,
                                  volFit=0.9, surFit=0.1)

        stem.setDescendants(0.98, [stem.id, basal.id])
        stem.setDescendants(0.01, [stem.id, stem.id])
        stem.setDescendants(0.01, [basal.id, basal.id])

        cellTypes.extend((medium, basalmembrane, stem, basal, intermediate, umbrella))

        return cellTypes
