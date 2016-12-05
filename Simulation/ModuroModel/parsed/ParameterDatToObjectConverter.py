# todo: load parameter Dat and parse Data
# parses parameterDump.dat and returns CellTypes and other values

from Core import CellType

class ParameterDumpToObjectsConverter:
    def __init__(self):
        return

    def getStemCell(self, parameterdumppath):
        # todo  - parse parameterdump StemCell values
        stem = CellType.Stemcell

        #stem.setGrowthVolumePerDayRelVolume(parsedValue)

        # todo - call setters and set values for stemcell
        return stem

    def getMedium(self, parameterdumppath):
        # todo: parse
        medium = CellType.Medium

        # todo: call setters of medium set values
        return medium

    def getBasalmembrane(self, parameterdumppath):
        # todo: impl
        basalmembrane = CellType.Basalmembrane
        return basalmembrane

    def getBasalcell(self, parameterdumppath):
        # todo: impl
        basalCell = CellType.Basalcell
        return basalCell

    def getIntermediatecell(self, parameterdumppath):
        # todo: impl
        intermidateCell = CellType.Intermediatecell
        return intermidateCell

    def getUmbrellacell(self, parameterdumppath):
        # todo: impl
        umbrellaCell = CellType.Umbrellacell
        return umbrellaCell

    def getNameOfModel(self, parameterdumppath):
        # todo: parse name of model
        nameOfModel = "ERROR MISSING"
        return  nameOfModel
