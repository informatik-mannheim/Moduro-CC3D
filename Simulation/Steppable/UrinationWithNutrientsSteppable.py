from Steppable.UrinationSteppable import UrinationSteppable

class UrinationSteppableWithNutrients(UrinationSteppable):
    def __init__(self, _simulator,  model, prop=0.02, _frequency=1):
        UrinationSteppable.__init__(self, _simulator, model, _frequency)

    def moduroStep(self, mcs):
        if mcs > 2 * self.urinationMCS and mcs % self.urinationMCS == 0:
            self.scalarField = self.getConcentrationField('Nutrients')
            for x, y, z in self.everyPixel():
                cell = self.cellField[x, y, z]
                if not cell:
                    self.scalarField[x, y, z] = 0
            self.removeCells() # also remove cells.