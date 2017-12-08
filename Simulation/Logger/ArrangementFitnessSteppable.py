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

from Logger.TissueFitnessSteppable import TissueFitnessSteppable


class ArrangementFitnessSteppable(TissueFitnessSteppable):
    def __init__(self, simulator, model, _frequency=1):
        TissueFitnessSteppable.__init__(self, simulator, model,
                                        "FitnessArrangement.dat", _frequency)

'''The method step implements the Arrangement fitness function -> see published paper section 4.3.1'''
    # step is overwritten
    # TODO sizes do not scale yet!
    def step(self, mcs):
        if self.execConfig.interuptMCS(mcs):
            deltaXPx = self.execConfig.calcPixelFromMuMeterMin1(20)  # 20 mu m.
            deltaZPx = deltaXPx
            sumFitness_a = []
            avgStemCellDiameterPx = \
                self.execConfig.calcPixelFromMuMeterMin1(self.model.cellTypes[2].getAvgDiameter())
            zRange = [0] if self.execConfig.zDimension == 1 else range(0, self.execConfig.zDimension, deltaZPx)
            for z in zRange:
                for x in xrange(1, self.execConfig.xDimension, deltaXPx):
                    cells_in_order = []
                    for y in xrange(3, self.execConfig.yDimension, int(avgStemCellDiameterPx / 2)):
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
                        '''
                        firstLayer & lastLayer are Boolean with the value 1 (true) and 0 (false)
                        '''
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
                        lib = 0 if layers == 0 else (layers - layersInBetween) / layers
                        fitness_a = 1.0 - (
                            (1.0 - float(firstLayer)) +
                            (1.0 - float(lastLayer)) +
                            lib +
                            (1.0 - float(optimumLayers))) / 4.0
                    sumFitness_a.append(fitness_a)


            fitness_a = sum(sumFitness_a) / len(sumFitness_a)
            self._addLine(mcs, fitness_a)
            print "!!!!!!!!!!!!!!!!! x: ", x, " steps: ", " fitness_a: ", fitness_a


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
