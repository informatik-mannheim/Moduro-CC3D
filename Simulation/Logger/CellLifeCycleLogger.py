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

__author__ = "Markus Gumbel"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Production"


class CellLifeCycleLogger(object):

    cells = {} # For plausibility check.

    def __init__(self, model, fileName):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Konstruktor CellLifeCycleLogger'
        self.model = model
        self.execConfig = model.execConfig
        self._fileName = fileName
        for i in range(999999):
            self.cells[i] = False # Set map with cell Ids to false.

    def _openFile(self):
        try:
            import CompuCellSetup
            fileHandle, fullFileName = CompuCellSetup.openFileInSimulationOutputDirectory(self._fileName, "a")
        except IOError:
            print "Could not open file ", self._fileName, \
                " for writing. Check if you have necessary permissions."

        return fileHandle

    # cellDict must be passed because the method is not available in this class.
    def cellLifeCycleBirth(self, timeMCS, cell, cellDict):
        fileHandle = self._openFile()
        timeDays = self.execConfig.calcDaysFromMCS(timeMCS)
        id = cellDict['id']
        fileHandle.write("%s " % timeDays)
        fileHandle.write("%s " % "+")
        fileHandle.write("%s " % id)
        fileHandle.write("%s " % cell.type)
        fileHandle.write("\n")
        fileHandle.close
        if (self.cells[id] == True):
            print "Cell ", id, " cannot be added twice!"
            raise
        else:
            self.cells[id] = True # Mark this cell (id) as being added.
        #print "QQQQQQQQQQQQQQ Logger: birth", timeDays, " ", id, " ", cell.type

    def cellLifeCycleDeath(self, timeMCS, cell, cellDict):
        if not cellDict['removed']:
            cellDict['removed'] = True
            fileHandle = self._openFile()
            timeDays = self.execConfig.calcDaysFromMCS(timeMCS)
            id = cellDict['id']
            lifeTime = self.execConfig.calcHoursFromMCS(cellDict['life_time'])
            fileHandle.write("%s " % timeDays)
            fileHandle.write("%s " % "-")
            fileHandle.write("%s " % id)
            fileHandle.write("%s " % cell.type)
            fileHandle.write("%s " % lifeTime)
            fileHandle.write("\n")
            fileHandle.close
            if (self.cells[id] == False):
                print "Cell ", id, " cannot be removed when not added!"
                raise
        #print "QQQQQQQQQQQQQQ Logger: death", timeDays, " ", id, " ", cell.type, " ", lifeTime
