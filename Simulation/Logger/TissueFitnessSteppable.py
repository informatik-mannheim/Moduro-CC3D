# Copyright 2016 the original author or authors.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

__author__ = "Angelo Torelli, Markus Gumbel"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Production"

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

    def _addLine(self, *args):
        fileHandle = self._openFile()
        for count, value in enumerate(args):
            if count == 0:
                fileHandle.write("%s " % self.execConfig.calcDaysFromMCS(value))
            else:
                fileHandle.write("%s " % value)
        fileHandle.write("\n")
        fileHandle.close()
