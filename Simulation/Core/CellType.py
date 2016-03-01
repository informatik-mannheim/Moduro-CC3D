from math import pi as PI
import random
from Core.ParameterStore import ParameterStore

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



