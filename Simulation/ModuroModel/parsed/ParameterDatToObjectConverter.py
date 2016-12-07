# todo: load parameter Dat and parse Data
# parses parameterDump.dat and returns CellTypes and other values

from Core import CellType
from Core.ParameterStore import ParameterStore

class ParameterDumpToObjectsConverter:

    paramDumpPath = 'ParameterDump.dat'
    # paramStore = ParameterStore()

    def __init__(self):
        return

    def getStemCell(self, paramDumpPath, paramStore):
        # todo  - parse parameterdump StemCell values
        paramStore = ParameterStore()
        stem = CellType.Stemcell

        stem.apoptosisTimeInDays = paramStore.readParameterfile(paramDumpPath).get('stem_apoptosisTimeInDays')
        self.necrosisProbStem = stem.necrosisProb = 0.0


        return stem

    def getMedium(self, paramDumpPath):
        # todo: parse
        medium = CellType.Medium

        # todo: call setters of medium set values
        return medium

    def getBasalmembrane(self, paramDumpPath):
        # todo: impl
        basalmembrane = CellType.Basalmembrane
        return basalmembrane

    def getBasalcell(self, paramDumpPath):
        # todo: impl
        basalCell = CellType.Basalcell
        return basalCell

    def getIntermediatecell(self, paramDumpPath):
        # todo: impl
        intermidateCell = CellType.Intermediatecell
        return intermidateCell

    def getUmbrellacell(self, paramDumpPath):
        # todo: impl
        umbrellaCell = CellType.Umbrellacell
        return umbrellaCell

    def getNameOfModel(self, paramDumpPath):
        # todo: parse name of model
        nameOfModel = "ERROR MISSING"
        return nameOfModel
