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

__author__ = "Angelo Torelli"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Production"

import random
from Steppable.ModuroSteppable import ModuroSteppable

class ColonySteppable(ModuroSteppable):
    def __init__(self, simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, simulator, model, _frequency)
        self.scalarCLField = self.createScalarFieldCellLevelPy("ColonyField")

    def moduroStep(self, mcs):
        if (self.model.execConfig.colonyTagInMCS - 2) <= mcs <= (self.model.execConfig.colonyTagInMCS + 2):
            cellNr = self.cellList.__len__()
            stemNr = 0
            for cell in self.cellList:
                if cell.type == self.STEM:
                    stemNr += 1
            distance = cellNr/stemNr
            for cell in self.cellList:
                if cell.type == self.STEM:
                    cellDict['colony'] = cellNr - stemNr * distance
                    stemNr -=1
                cellDict = self.getDictionaryAttribute(cell)
                cellDict['colony'] = cell.id
        elif self.model.execConfig.colonyTagInMCS + 10 < mcs:
            self.model.execConfig.colonyTag = True
            self.scalarCLField.clear()
            for cell in self.cellList:
                cellDict = self.getDictionaryAttribute(cell)
                self.scalarCLField[cell] = cellDict['colony']

