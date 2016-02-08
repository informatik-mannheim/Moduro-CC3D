import random
from Steppable.ModuroSteppable import ModuroSteppable

class GrowthSteppable(ModuroSteppable):
    def __init__(self, simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, simulator, model, _frequency)

    def moduroStep(self, mcs):
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            cellType = self.model.cellTypes[cell.type]
            # print "!!!!!! cell.tvol=", cell.targetVolume, "<=type.tVol=", cellDict['target_Volume']

            # DEPENDS ON HOW MUCH A MCS IS
            cellDict['life_time'] += 1
            apoptosisMCS = self.execConfig.calcMCSfromDays(cellType.apoptosisTimeInDays)
            if cellDict['life_time'] >= apoptosisMCS:
                cellDict['necrosis'] = [True]
            elif cellType.divides or cellType.transforms and \
                            cell.targetVolume <= cellDict['target_Volume']:
                cell.targetSurface = self.execConfig.calcVoxelSurfaceFromVoxelVolume(cell.volume)
                # print "! ! ! ! tSurf=", cell.targetSurface

                # TODO: necrosis trigger if to little nutrients
                # Growth (mu m^3 ) per MCS:
                deltaVolPerMCS = 1.0 * cellType.growthVolumePerDay / self.execConfig.MCSperDay
                # Volume/surface change in voxel per day.
                deltaVolDimPerDay = self.execConfig.calcVoxelVolumeFromVolume(cellType.growthVolumePerDay)
                deltaVolDimPerMCS = 1.0 * deltaVolDimPerDay / self.execConfig.MCSperDay
                if deltaVolDimPerMCS < 1.0: # The change may be too small for one MCS.
                    deltaVolDimPerMCS = 1 if deltaVolDimPerMCS >= random.random() else 0

                #print "!!::!::!:!:! deltaVol=", deltaVolPerMCS, ", deltaVolDimPerDay=",\
                #    deltaVolDimPerDay, ", deltaVolDimPerMCS=", deltaVolDimPerMCS
                cell.targetVolume += deltaVolDimPerMCS
