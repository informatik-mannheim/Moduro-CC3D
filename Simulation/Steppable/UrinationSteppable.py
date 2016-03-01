import random
from Steppable.ModuroSteppable import ModuroSteppable

class UrinationSteppable(ModuroSteppable):
    def __init__(self, _simulator,  model, prop=0.02, _frequency=1):
        ModuroSteppable.__init__(self, _simulator, model, _frequency)
        self.urinationMCS = self.execConfig.calcMCSfromDays(0.25) # every six hours.
        self.deathIntervalMCS = self.execConfig.calcMCSfromDays(1) # one day.
        self.prop = prop

    def moduroStep(self, mcs):
        if mcs > 2 * self.urinationMCS and mcs % self.urinationMCS == 0:
            # print "URINATION !!!!!!!!!!!!!!!!!!!! at ", mcs
            self._removeCells()

    def _removeCells(self):
        for cell in self.cellList:
            totalArea = 0
            cell.lambdaVecX = 0
            for neighbor, commonSurfaceArea in self.getCellNeighborDataList(cell):
                if not neighbor:
                    totalArea += commonSurfaceArea
            if totalArea > 0 and random.random() < self.prop:
                # print "WEG!!!!!!!!!!!!!!!!!!!"
                cellDict = self.getDictionaryAttribute(cell)
                # TODO was happens here?
                cell.lambdaVecY = 0 # -500
                apoptosisDays = self.model.cellTypes[cell.type].apoptosisTimeInDays
                killTime = self.execConfig.calcMCSfromDays(apoptosisDays)
                cellDict['life_time'] = killTime - self.deathIntervalMCS