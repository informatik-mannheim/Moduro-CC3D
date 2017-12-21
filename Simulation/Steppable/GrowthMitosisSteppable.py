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

from Steppable.ModuroMitosisSteppable import ModuroMitosisSteppable


class GrowthMitosisSteppable(ModuroMitosisSteppable):
    def __init__(self, _simulator, model, splitPercentage=1.95,_frequency=1):
        print'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! in Konstruktor von GrowthMitosisStepable - splitPercentage {}'.format(splitPercentage)
        self.splitPercentage = splitPercentage
        ModuroMitosisSteppable.__init__(self, _simulator, model, _frequency)

    def moduroStep(self, mcs):
        cells_to_divide = []
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            cellType = self.model.cellTypes[cell.type]

            if cellType.divides and \
                    cell.volume >= self.splitPercentage * cellDict['normal_volume'] and \
                    not cellDict['necrosis']:
                print '!!!!!!!!!!!!!!!!!!!!!!!!! cellDivision'
                print cellDict['normal_volume']
                print 'cellID {} - cellType {} - cellVolume {} - cellTargetVolume {}'.format(cellDict['id'], cell.type,
                                                                                             cell.volume,
                                                                                              cell.targetVolume)
                # Register death
                self._cellLifeCycleDeath(cell)
                cells_to_divide.append(cell)
                self.divideCellRandomOrientation(cell)


    def updateAttributes(self):
        parentCell = self.mitosisSteppable.parentCell
        childCell = self.mitosisSteppable.childCell

        #Has to be done this way otherwise if cell.volume is chosen than it disappears
        newVol = parentCell.targetVolume / 2

        descendents = self.model.cellTypes[parentCell.type].getDescendants()
        parentCell.type = descendents[0]
        childCell.type = descendents[1]

        # Now set the attributes for the two daughter cells:
        cellDictChild = self.getDictionaryAttribute(childCell)
        self.model.initCellAttributes(childCell, cellDictChild)
        cellDictParent = self.getDictionaryAttribute(parentCell)
        self.model.initCellAttributes(parentCell, cellDictParent)

        parentCell.targetVolume = newVol
        childCell.targetVolume = newVol

        # Register events
        print '!!!!!!!!!!!!!!!!!!!!!!!!! parentCell'
        self._cellLifeCycleBirth(parentCell)
        print '!!!!!!!!!!!!!!!!!!!!!!!!! childCell'
        self._cellLifeCycleBirth(childCell)
        cellDictChild['colony'] = cellDictParent['colony']
