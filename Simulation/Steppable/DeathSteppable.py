import random
from Steppable.ModuroSteppable import ModuroSteppable

class DeathSteppable(ModuroSteppable):
    def __init__(self, _simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, _simulator, model,_frequency)

    def moduroStep(self, mcs):
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            if cellDict['necrosis'] == True:
                #print "!!!!!!!!!!!!!!!!!!!!! NECROSIS", cell
                if cell.targetVolume > 5:
                    #TODO: find an equation for timeless cell reduction
                    targetVolume = float(cellDict['target_Volume'])
                    deltaVolDimPerMCS = 100.0 * targetVolume / self.execConfig.MCSperDay
                    if deltaVolDimPerMCS < 1.0: # The change may be too small for one MCS.
                        deltaVolDimPerMCS = 1 if deltaVolDimPerMCS >= random.random() else 0
                    cell.targetVolume -= deltaVolDimPerMCS
                else:
                    cell.targetVolume = 0
                cell.lambdaVolume = 1000 # TODO Force cell to have 0 pixel!