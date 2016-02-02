__author__ = 'Angelo'

class CellLineage(object):

    def __init__(self, model):
        self.model = model

    def getDaughter(self, celltype):
        if celltype.name == "Stem":
            return self.model.cellType("Basal")

    def isDifferentiated(cell):
        return None


