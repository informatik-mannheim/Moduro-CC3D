from Steppable.GrowthSteppable import GrowthSteppable

class NutrientGrowthSteppable(GrowthSteppable):
    def __init__(self, simulator, execConfig, model, _frequency=1):
        GrowthSteppable.__init__(self, simulator, execConfig, model, _frequency)

    def moduroStep(self, mcs):
        self.scalarField = self.getConcentrationField('Nutrients')
        for cell in self.cellList:
            cellType = self.model.cellTypes[cell.type]
            cellDict = self.getDictionaryAttribute(cell)
            #DEPENDS ON HOW MUCH A MCS IS
            cellDict['life_time'][0] += 1
            if cellDict['life_time'][0] >= \
                self.execConfig.calcMCSfromDays(cellType.apoptosisTimeInDays):
                cellDict['necrosis'] = [True]
            totalNutrients = 0
            if not cellType.frozen:
                pixelList = self.getCellPixelList(cell)
                for pixelTrackerData in pixelList:
                    totalNutrients += self.scalarField[
                        pixelTrackerData.pixel.x, pixelTrackerData.pixel.y, pixelTrackerData.pixel.z]
                    #TODO: bring the consumption per cell constant into central place
                    if self.scalarField[pixelTrackerData.pixel.x,
                                        pixelTrackerData.pixel.y,
                                        pixelTrackerData.pixel.z] > 0.003 / self.execConfig.MCSperDay:
                        self.scalarField[pixelTrackerData.pixel.x,
                                         pixelTrackerData.pixel.y,
                                         pixelTrackerData.pixel.z] -= 0.003 / self.execConfig.MCSperDay
                    else:
                        self.scalarField[pixelTrackerData.pixel.x,
                                         pixelTrackerData.pixel.y,
                                         pixelTrackerData.pixel.z] = 0
            if cellType.divides or cellType.differentiates and cell.targetVolume <= cellDict['target_Volume'][0]:
                cell.targetSurface = self.execConfig.calcVoxelSurfaceFromVoxelVolume(cell.volume)
                #TODO: necrosis trigger if to little nutrients
                if totalNutrients >= cellType.nutrientRequirement * cell.volume:
                    # TODO formula wrong; same story as in GrothSteppable:
                    cell.targetVolume += cellType.growthVolumePerDay / self.execConfig.MCSperDay




