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
    def __init__(self, _simulator, model, _frequency=1):
        ModuroMitosisSteppable.__init__(self, _simulator, model, _frequency)

    def moduroStep(self, mcs):
        cells_to_divide = []
        for cell in self.cellList:
            cellDict = self.getDictionaryAttribute(cell)
            cellType = self.model.cellTypes[cell.type]

            # TODO: extract the constant 1.3 out of code into central place
            if cellType.divides and \
                    cell.volume > 1.3 * cellDict['target_Volume'] and \
                    not cellDict['necrosis']:
                cells_to_divide.append(cell)
                self.divideCellRandomOrientation(cell)

    def updateAttributes(self):
        parentCell = self.mitosisSteppable.parentCell
        childCell = self.mitosisSteppable.childCell
        parentCell.targetVolume = parentCell.targetVolume / 2
        childCell.targetVolume = parentCell.targetVolume / 2

        descendents = self.model.cellTypes[parentCell.type].getDescendants()
        parentCell.type = descendents[0]
        childCell.type = descendents[1]

        # Now set the attributes for the two daughter cells:
        cellDict = self.getDictionaryAttribute(childCell)
        self.model.setCellAttributes(cellDict, childCell, 0)
        childCell.lambdaVolume = \
            self.execConfig.calcVolLambdaFromVolFit(cellDict['volume_lambda'])
        childCell.lambdaSurface = \
            self.execConfig.calcSurLambdaFromSurFit(cellDict['surface_lambda'])

        self.model.setCellAttributes(cellDict, parentCell, 0)
        cellDict = self.getDictionaryAttribute(parentCell)
        parentCell.lambdaVolume = \
            self.execConfig.calcVolLambdaFromVolFit(cellDict['volume_lambda'])
        parentCell.lambdaSurface = \
            self.execConfig.calcSurLambdaFromSurFit(cellDict['surface_lambda'])
