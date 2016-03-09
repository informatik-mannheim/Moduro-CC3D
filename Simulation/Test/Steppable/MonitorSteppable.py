from Steppable.ModuroSteppable import ModuroSteppable

class MonitorSteppable(ModuroSteppable):
    def __init__(self, _simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, _simulator, model,_frequency)

    def moduroStep(self, mcs):
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            print "!!!!!! VOL !!!!! tVol_s=", cell.targetVolume, \
                ", tVol_i=",cell.volume, "=", cellDict['target_Volume']
            print "tSur_i=", cell.surface, "=", cell.targetSurface  #, "=", cellDict['target_Surface']
