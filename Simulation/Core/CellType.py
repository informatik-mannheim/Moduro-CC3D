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
                 volFit=1.0, surFit=0.0,
                 differentiates=True, asym=1.0, idenSym=0.0, diffSym=0.0):
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
        :param differentiates:
        :param asym:
        :param idenSym:
        :param diffSym:
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
        self.differentiates = differentiates
        self.asym = asym
        self.idenSym = idenSym
        self.diffSym = diffSym
        if asym + idenSym + diffSym == 0.0:
            self.divides = False
        else:
            self.divides = True
        CellType.__typeCount += 1

    def getAvgVolume(self):
        return (self.minVol + self.maxVol) / 2.0

    def getAvgDiameter(self):
        return (self.minDiameter + self.maxDiameter) / 2.0
