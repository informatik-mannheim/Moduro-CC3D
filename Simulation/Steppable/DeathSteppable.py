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

import random
from Steppable.ModuroSteppable import ModuroSteppable

class DeathSteppable(ModuroSteppable):
    def __init__(self, _simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, _simulator, model,_frequency)

    def moduroStep(self, mcs):
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            if cellDict['necrosis'] == True:
                #print "!!!!!!!!!!!!!!!!!!!!! NECROSIS", cell
                if cell.targetVolume > 5:
                    #TODO: find an equation for timeless cell reduction
                    targetVolume = float(cellDict['target_Volume'])
                    deltaVolDimPerMCS = 100.0 * targetVolume / self.execConfig.MCSperDay
                    if deltaVolDimPerMCS < 1.0: # The change may be too small for one MCS.
                        deltaVolDimPerMCS = 1 if deltaVolDimPerMCS >= random.random() else 0
                    cell.targetVolume -= deltaVolDimPerMCS
                else:
                    cell.targetVolume = 0
                cell.lambdaVolume = 1000 # TODO Force cell to have 0 pixel!