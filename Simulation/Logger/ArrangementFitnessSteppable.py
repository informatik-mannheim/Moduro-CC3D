from Logger.TissueFitnessSteppable import TissueFitnessSteppable


class ArrangementFitnessSteppable(TissueFitnessSteppable):
    def __init__(self, simulator, model, _frequency=1):
        TissueFitnessSteppable.__init__(self, simulator, model,
                                        "FitnessArrangement.dat", _frequency)

    # step is overwritten
    # TODO sizes do not scale yet!
    def step(self, mcs):
        if self.execConfig.interuptMCS(mcs):
            sumFitness_a = []
            ratio = float(self.execConfig.xDimension) / float(self.execConfig.yDimension) \
                if self.execConfig.xDimension < self.execConfig.yDimension \
                else float(self.execConfig.yDimension) / float(self.execConfig.xDimension)
            avgStemCellDiameter = self.model.cellTypes[2].getAvgDiameter()
            zRange = [0] if self.execConfig.zDimension == 1 else range(0, self.execConfig.zDimension, int(ratio * self.execConfig.zDimension))
            for z in zRange:
                for x in xrange(1, self.execConfig.xDimension, int(ratio * self.execConfig.xDimension)):
                    cells_in_order = []
                    for y in xrange(3, self.execConfig.yDimension, int(avgStemCellDiameter/2)):
                        # Gives the mode of a cell ID in a 3x3x3 pixels cube if 3D otherwise 3x3 rectangle
                        mode_of_cellIDs = []
                        for width in xrange(0, 2, 1):
                            for height in xrange(0, 2, 1):
                                depthRange = [0] if zRange.__len__() == 1 else range(0, 2, 1)
                                for depth in depthRange:
                                    if self.cellField[x + width, y + height, z + depth] is not None:
                                        mode_of_cellIDs.append(self.cellField[x + width, y + height, z + depth].id)
                        # If mode ID exists and in not already in cell_in_order list it will be added
                        if len(mode_of_cellIDs) > 0:
                            cellToCheck = self.attemptFetchingCellById(self.mode(mode_of_cellIDs))
                            exist = False
                            for cell in cells_in_order:
                                if cellToCheck.id == cell.id:
                                    exist = True
                            if not exist:
                                cells_in_order.append(cellToCheck)
                    layers = len(cells_in_order)
                    if layers == 0:
                        fitness_a = 0
                    else:
                        optimumLayers = 1 if layers <= 7 and layers >= 3 else 0
                        if cells_in_order[layers - 1].type == self.UMBRELLA:
                            lastLayer = 1
                            layers -= 1
                        else:
                            lastLayer = 0
                        if cells_in_order[0].type == self.STEM or cells_in_order[0].type == self.BASAL:
                            firstLayer = 1
                            layers -= 1
                        else:
                            firstLayer = 0
                        layersInBetween = layers
                        for x in range(firstLayer, len(cells_in_order) - 1 - lastLayer, 1):
                            if cells_in_order[x].type != self.INTERMEDIATE:
                                layersInBetween -= 1
                        fitness_a = 1.0 / (
                            (1.0 - float(firstLayer)) +
                            (1.0 - float(lastLayer)) +
                            (layers - layersInBetween) +
                            (1.0 - float(optimumLayers)) + 1.0)
                    sumFitness_a.append(fitness_a)
                    # print "!!!!!!!!!!!!!!!!! x: ", x, " steps: ", int(ratio * self.execConfig.xDimension), " fitness_a: ", fitness_a

            fitness_a = sum(sumFitness_a) / len(sumFitness_a)
            self._addLine(mcs, fitness_a)

    def mode(self, IDs):
        """
        Returns the mode of the IDs in a certain region.
        :param IDs:
        :return:
        """
        corresponding = {}
        occurances = []
        for i in IDs:
            count = IDs.count(i)
            corresponding.update({i: count})

        for i in corresponding:
            freq = corresponding[i]
            occurances.append(freq)

        maxFreq = max(occurances)

        keys = corresponding.keys()
        values = corresponding.values()

        index_v = values.index(maxFreq)
        mode = keys[index_v]
        return mode
