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

from Steppable.UrinationSteppable import UrinationSteppable

class UrinationWithNutrientsSteppable(UrinationSteppable):
    def __init__(self, _simulator,  model, prop=0.02, _frequency=1):
        UrinationSteppable.__init__(self, _simulator, model, prop, _frequency)

    def moduroStep(self, mcs):
        if mcs > 2 * self.urinationMCS and mcs % self.urinationMCS == 0:
            self.scalarField = self.getConcentrationField('Nutrients')
            for x, y, z in self.everyPixel():
                cell = self.cellField[x, y, z]
                if not cell:
                    self.scalarField[x, y, z] = 0
            self._removeCells() # also remove cells.