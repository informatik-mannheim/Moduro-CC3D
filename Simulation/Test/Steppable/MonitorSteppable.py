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
__status__ = "Test"

from Steppable.ModuroSteppable import ModuroSteppable

class MonitorSteppable(ModuroSteppable):
    def __init__(self, _simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, _simulator, model,_frequency)

    def moduroStep(self, mcs):
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            perc = cell.volume / cellDict['normal_volume']
            print "!!!!!! VOL !!!!! tVol_s=", cell.targetVolume, \
                "~ tVol_i=", cell.volume, ">=", cellDict['normal_volume'], " =Vol_n", \
                " (", perc, ")"
            print "tSur_i=", cell.surface, "=", cell.targetSurface  #, "=", cellDict['target_Surface']
