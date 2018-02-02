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

__author__ = "Markus Gumbel, Julian Debatin"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Production"

import random
from Steppable.ModuroSteppable import ModuroSteppable
from Core.CellType import *

class MutationSteppable(ModuroSteppable):
    def __init__(self, _simulator,  model, probStem=0.00, probBasal=0.00, probIntermediate=0.00, probUmbrella=0.00, _frequency=1):
        ModuroSteppable.__init__(self, _simulator, model, _frequency)
        self.mutationMCS = self.execConfig.calcMCSfromDays(1) # every day.
        self.probStem = probStem
        self.probBasal = probBasal
        self.probIntermediate = probIntermediate
        self.probUmbrella = probUmbrella

    def moduroStep(self, mcs):
        if mcs > 2 * self.mutationMCS: #and mcs % self.mutationMCS == 0: - after 1000 MCS use it
            self._removeCells()

    def _removeCells(self):
        for cell in self.cellList:
            if cell.type == self.STEM:
                if random.random() < self.probStem:  # Random float x, 0.0 <= x < 1.0
                    cellDict = self.getDictionaryAttribute(cell)
                    cellDict['necrosis'] = True
            elif cell.type == self.BASAL:
                if random.random() < self.probBasal:
                    cellDict = self.getDictionaryAttribute(cell)
                    cellDict['necrosis'] = True
            elif cell.type == self.INTERMEDIATE:
                if random.random() < self.probIntermediate:
                    cellDict = self.getDictionaryAttribute(cell)
                    cellDict['necrosis'] = True
            elif cell.type == self.UMBRELLA:
                if random.random() < self.probUmbrella:
                    cellDict = self.getDictionaryAttribute(cell)
                    cellDict['necrosis'] = True