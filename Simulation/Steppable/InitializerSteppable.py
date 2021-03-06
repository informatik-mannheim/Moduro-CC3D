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

class InitializerSteppable(ModuroSteppable):
    def __init__(self, simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, simulator, model, _frequency)

    def start(self):
        """
        Initialize all cells.
        :return:
        """
        # Required here! Otherwise CC3D will not create the file.
        #self.execConfig.parameterStore.saveParameterfile("ParameterDump.dat")
        self.execConfig.parameterStore.saveAllObjs("ParameterDump.dat")

        self.model._initCells(self)


        for cell in self.cellList:
            # cellDict needs to be retrieved in a steppable:
            cellDict = self.getDictionaryAttribute(cell)
            self.model.initCellAttributes(cell, cellDict)
            self.model.cellLifeCycleLogger.cellLifeCycleBirth(0, cell, cellDict)

            cellType = self.model.cellTypes[cell.type]

