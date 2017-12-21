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
import Math


class CellType(object):
    """
    A cell type.
    """
    __typeCount = 0
    consumPerCell = 0.003

    # TODO explain parameter
    def __init__(self, name="CellType", frozen=False, minDiameter=10, maxDiameter=10,
                 growthVolumePerDay=500, nutrientRequirement=1.0, apoptosisTimeInDays=180000,
                 #volFit=1.0, surFit=0.0,
                 necrosisProb=0.0):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!! In Konstruktor CellType'

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
        :param necrosisProb: propability for a cell to do necrosis
        :return:
        """
        self.id = CellType.__typeCount
        self.name = name
        self.frozen = frozen
        self.minDiameter = minDiameter
        self.maxDiameter = maxDiameter
        self.minVol = 4.0 / 3.0 * PI * (self.minDiameter / 2.0) * (self.minDiameter / 2.0) * (self.minDiameter / 2.0)
        self.maxVol = 4.0 / 3.0 * PI * (self.maxDiameter / 2.0) * (self.maxDiameter / 2.0) * (self.maxDiameter / 2.0)
        self.growthVolumePerDay = growthVolumePerDay
        self.nutrientRequirement = nutrientRequirement
        self.apoptosisTimeInDays = apoptosisTimeInDays
        #self.volFit = volFit
        #self.surFit = surFit
        self.divides = False
        self.descendants = []
        self.necrosisProb = necrosisProb
        CellType.__typeCount += 1

    def setGrowthVolumePerDayRelVolume(self, multiple):
        print '------------------------------------------------------------------ In Function CellType.setGrowthVolumePerDayRelVolume'
        print'!!!! maxDiameter {}'.format(self.maxDiameter)
        '''
        Set the growth volume per day relative to the maximum cell volume.
        :param multiple: Factor for the daily growth.
        :return:
        '''
        self.growthVolumePerDay = multiple * Math.calcSphereVolumeFromDiameter(self.maxDiameter)

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
        # TODO: check if probability is higher than 1.0 and normalize
        cellLineageOfCellType = [probability, descendants]
        self.descendants.append(cellLineageOfCellType)
        self.divides = True


# Some frequently reused objects:

Medium = CellType(name="Medium", frozen=True, minDiameter=0, maxDiameter=0,
                  growthVolumePerDay=0, nutrientRequirement=0, apoptosisTimeInDays=0)
                  #volFit=1.0, surFit=1.0

Basalmembrane = CellType(name="BasalMembrane", frozen=True, minDiameter=0, maxDiameter=0,
                         growthVolumePerDay=0, nutrientRequirement=0, apoptosisTimeInDays=180000)
                         #volFit=1.0, surFit=1.0)

Stemcell = CellType(name="Stem", minDiameter=8, maxDiameter=10,
                    growthVolumePerDay=1 * Math.calcSphereVolumeFromDiameter(10),
                    nutrientRequirement=1.0, apoptosisTimeInDays=180000)
                    #volFit=0.9, surFit=0.5)

Basalcell = CellType(name="Basal", minDiameter=9, maxDiameter=10,
                     growthVolumePerDay=1 * Math.calcSphereVolumeFromDiameter(10),
                     nutrientRequirement=1.0, apoptosisTimeInDays=80)
                     #volFit=0.9, surFit=0.5)

Intermediatecell = CellType(name="Intermediate", minDiameter=12, maxDiameter=15,
                            growthVolumePerDay=1 * Math.calcSphereVolumeFromDiameter(15),
                            nutrientRequirement=1.0, apoptosisTimeInDays=2)
                            #volFit=0.9, surFit=0.1)

Umbrellacell = CellType(name="Umbrella", minDiameter=15, maxDiameter=19,
                        growthVolumePerDay=1 * Math.calcSphereVolumeFromDiameter(19),
                        nutrientRequirement=1.0, apoptosisTimeInDays=2)
                        #volFit=0.9, surFit=0.1)

