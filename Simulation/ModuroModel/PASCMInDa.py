from Core.CellType import CellType
from Core.ExecConfig import ExecConfig
from Core.ModelConfig import ModelConfig
from ModuroModel.CMInDa import CMInDa


class PASCMInDa(CMInDa):
    def __init__(self, sim, simthread, srcDir):
        ModelConfig.__init__(self, sim, simthread, srcDir)

    def _initModel(self):
        self.name = "PASCMInDa"
        self.adhFactor = 0.5  # average adhesion = 0.5
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


        stem.setDescendants(0.98, [stem, basal])
        stem.setDescendants(0.01, [stem, stem])
        stem.setDescendants(0.01, [basal, basal])
        basal.setDescendants(1.0, [intermediate])
        intermediate.setDescendants(1.0, [umbrella])

        cellTypes.extend((medium, basalmembrane, stem, basal, intermediate, umbrella))

        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + str([a for a in dir(cellTypes[0]) if not a.startswith('_') and not callable(getattr(cellTypes[0],a))])
        return cellTypes

    def _createExecConfig(self, srcDir):
        return ExecConfig(srcDir=srcDir,
                          xLength=800, yLength=100, zLength=0, voxelDensity=0.8,
                          MCSperDay=500)
