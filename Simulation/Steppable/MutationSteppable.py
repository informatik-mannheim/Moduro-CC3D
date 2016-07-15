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

import random
from Steppable.ModuroSteppable import ModuroSteppable

class MutationSteppable(ModuroSteppable):
    def __init__(self, _simulator,  model, prob=0.01, _frequency=1):
        ModuroSteppable.__init__(self, _simulator, model, _frequency)
        self.mutationMCS = self.execConfig.calcMCSfromDays(1) # every six hours.
        self.prob = prob

    def moduroStep(self, mcs):
        if mcs > 2 * self.mutationMCS and mcs % self.mutationMCS == 0:
            self._removeCells()

    def _removeCells(self):
        for cell in self.cellList:
            if random.random() < self.prob:
                cellDict = self.getDictionaryAttribute(cell)
                cellDict['necrosis'] = True