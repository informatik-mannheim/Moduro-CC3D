from Steppable.ModuroSteppable import ModuroSteppable


class TissueFitnessSteppable(ModuroSteppable):
    def __init__(self, simulator, model, fileName, _frequency=1):
        ModuroSteppable.__init__(self, simulator, model, _frequency)
        self.latticeSize = self.execConfig.latticeSizeInVoxel
        self._fileName = fileName

    def _openFile(self):
        try:
            import CompuCellSetup
            fileHandle, fullFileName = CompuCellSetup.openFileInSimulationOutputDirectory(self._fileName, "a")
        except IOError:
            print "Could not open file ", self._fileName, \
                " for writing. Check if you have necessary permissions."

        return fileHandle

    def _addLine(self, mcs, value):
        fileHandle = self._openFile()

        fileHandle.write("%s " % self.execConfig.calcDaysFromMCS(mcs))
        fileHandle.write("%s " % value)
        fileHandle.write("\n")
        fileHandle.close()
