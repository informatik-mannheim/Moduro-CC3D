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
from math import pi as PI


class CellType(object):
    """
    A cell type.
    """
    __typeCount = 0
    consumPerCell = 0.003

    # TODO explain parameter
    def __init__(self, name="CellType", frozen=False, minDiameter=10, maxDiameter=10,
                 growthVolumePerDay=500, nutrientRequirement=1.0, apoptosisTimeInDays=180000,
                 volFit=1.0, surFit=0.0):
        """

        :param name:
        :param frozen: True: cell is frozen, i.e. cannot move.
        :param minDiameter: Minimal diameter in mu m.
        :param maxDiameter: Maximal diameter in mu m.
        :param growthVolumePerDay: tbd. e.g. growth in percent per h or absolute per h.
        :param nutrientRequirement:
        :param apoptosisTimeInDays:
        :param volFit:
        :param surFit:
        :return:
        """
        self.id = CellType.__typeCount
        self.name = name
        self.frozen = frozen
        self.minDiameter = minDiameter
        self.maxDiameter = maxDiameter
        self.minVol = 4.0 / 3 * PI * ((minDiameter / 2) ** 3)
        self.maxVol = 4.0 / 3 * PI * ((maxDiameter / 2) ** 3)
        self.growthVolumePerDay = growthVolumePerDay
        self.nutrientRequirement = nutrientRequirement
        self.apoptosisTimeInDays = apoptosisTimeInDays
        self.volFit = volFit
        self.surFit = surFit
        self.divides = False
        self.descendants = []
        CellType.__typeCount += 1

    def getAvgVolume(self):
        return (self.minVol + self.maxVol) / 2.0

    def getAvgDiameter(self):
        return (self.minDiameter + self.maxDiameter) / 2.0

    def getDescendants(self):
        if self.divides:
            prob = random.random()
            for x in self.descendants:
                if prob < x[0]:
                    return [x[1][0], x[1][1]]
                else:
                    prob -= x[0]
        else:
            return []

    def setDescendants(self, probability, descendants):
        #TODO: check if probability is higher than 1.0 and normalize
        cellLineageOfCellType = [probability, descendants]
        self.descendants.append(cellLineageOfCellType)
        self.divides = True