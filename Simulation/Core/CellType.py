from math import pi as PI
import random

class CellType(object):
    """
    A cell type.
    """
    __typeCount = 0
    consumPerCell = 0.003

    # TODO explain parameter
    def __init__(self, name="CellType", frozen=False, minDiameter=10, maxDiameter=10,
                 growthVolumePerDay=500, nutrientRequirement=1.0, apoptosisTimeInDays=180000,
                 volFit=1.0, surFit=0.0, divides=False, transforms=False):
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
        :param transforms:
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
        self.divides = divides
        self.transforms = transforms
        self.descendants = []
        CellType.__typeCount += 1

    def getAvgVolume(self):
        return (self.minVol + self.maxVol) / 2.0

    def getAvgDiameter(self):
        return (self.minDiameter + self.maxDiameter) / 2.0

    def getDescendants(self):
        if self.divides or self.transforms:
            prob = random.random()
            for x in self.descendants:
                if self.__isLower(prob, x[0]):
                    return [x[1][0].id, x[1][1].id] if self.divides else [x[1][0].id]
                else:
                    prob -= x[0]
        else:
            return []

    def setDescendants(self, probability, descendants):
        #TODO: check if probability is higher than 1.0 and normalize
        cellLineageOfCellType = [probability, descendants]
        self.descendants.append(cellLineageOfCellType)

    def __isLower(self, prob1, prob2):
        if prob1 <= prob2:
            return True
        else:
            return False

