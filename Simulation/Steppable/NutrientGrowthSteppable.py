import random
from Steppable.GrowthSteppable import GrowthSteppable

class NutrientGrowthSteppable(GrowthSteppable):
    def __init__(self, simulator, model, _frequency=1):
        GrowthSteppable.__init__(self, simulator, model, _frequency)

    def moduroStep(self, mcs):
        self.scalarField = self.getConcentrationField('Nutrients')
        for cell in self.cellList:
            cellType = self.model.cellTypes[cell.type]
            cellDict = self.getDictionaryAttribute(cell)
            #DEPENDS ON HOW MUCH A MCS IS
            cellDict['life_time'] += 1
            apoptosisMCS = self.execConfig.calcMCSfromDays(cellType.apoptosisTimeInDays)
            if cellDict['life_time'] >= apoptosisMCS:
                cellDict['necrosis'] = [True]
            totalNutrients = 0
            if not cellType.frozen:
                pixelList = self.getCellPixelList(cell)
                for pixelTrackerData in pixelList:
                    totalNutrients += self.scalarField[
                        pixelTrackerData.pixel.x, pixelTrackerData.pixel.y, pixelTrackerData.pixel.z]
                    if self.scalarField[pixelTrackerData.pixel.x,
                                        pixelTrackerData.pixel.y,
                                        pixelTrackerData.pixel.z] > cellType.consumPerCell / self.execConfig.MCSperDay:
                        self.scalarField[pixelTrackerData.pixel.x,
                                         pixelTrackerData.pixel.y,
                                         pixelTrackerData.pixel.z] -= cellType.consumPerCell / self.execConfig.MCSperDay
                    else:
                        self.scalarField[pixelTrackerData.pixel.x,
                                         pixelTrackerData.pixel.y,
                                         pixelTrackerData.pixel.z] = 0
            if cellType.divides or cell.targetVolume <= cellDict['target_Volume']:
                cell.targetSurface = self.execConfig.calcVoxelSurfaceFromVoxelVolume(cell.volume)
                #TODO: necrosis trigger if to little nutrients
                if totalNutrients >= cellType.nutrientRequirement * cell.volume:
                    deltaVolDimPerDay = self.execConfig.calcVoxelVolumeFromVolume(cellType.growthVolumePerDay)
                    deltaVolDimPerMCS = 1.0 * deltaVolDimPerDay / self.execConfig.MCSperDay
                    if deltaVolDimPerMCS < 1.0: # The change may be too small for one MCS.
                        deltaVolDimPerMCS = 1 if deltaVolDimPerMCS >= random.random() else 0
                    cell.targetVolume += deltaVolDimPerMCS




