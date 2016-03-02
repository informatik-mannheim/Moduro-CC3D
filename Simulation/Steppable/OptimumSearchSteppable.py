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

__author__ = "Angelo Torelli"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Production"

from Steppable.ModuroSteppable import ModuroSteppable

class OptimumSearchSteppable(ModuroSteppable):
    def __init__(self, simulator, model, _frequency=1):
        ModuroSteppable.__init__(self, simulator, model, _frequency)
        self.idealUrotheliumVol = self.execConfig.xDimension * 85 * self.execConfig.zDimension
        self.idealBasalStemCellsVol = 0.1 * self.idealUrotheliumVol
        self.idealIntermediateCellsVol = 0.67 * self.idealUrotheliumVol
        self.idealUmbrellaCellsVol = 0.23 * self.idealUrotheliumVol
        self.latticeSize = self.execConfig.xDimension * self.execConfig.yDimension * self.execConfig.zDimension
        self.optimum = []

    # step is overwritten
    # TODO sizes do not scale yet!
    def step(self, mcs):
        if self.execConfig.interuptMCS(mcs):
            sumFitness_a = []
            totalVolume = 0
            umbrellaVolume = 0
            intermediateVolume = 0
            basalStemVolume = 0
            mediumVolume = self.latticeSize
            for cell in self.cellList:
                if cell.type == self.BASALMEMBRANE:
                    mediumVolume -= cell.volume
                if cell.type > self.BASALMEMBRANE:
                    totalVolume += cell.volume
                    if cell.type == self.UMBRELLA:
                        umbrellaVolume += cell.volume
                        mediumVolume -= cell.volume
                    elif cell.type == self.INTERMEDIATE:
                        intermediateVolume += cell.volume
                        mediumVolume -= cell.volume
                    else:
                        basalStemVolume += cell.volume
                        mediumVolume -= cell.volume
            if totalVolume == 0 or mediumVolume == 0:
                fitness_v = 0.0
                #print "No more cell in simulation"
                self.stopSimulation()
            else:
                fitness_v = ((self.latticeSize / ((float(
                    self.idealUmbrellaCellsVol) - float(umbrellaVolume))**2.0 / 3.0 + self.latticeSize)) + (
                    self.latticeSize / ((float(
                        self.idealIntermediateCellsVol) - float(intermediateVolume))**2.0 / 3.0 + self.latticeSize)) +  (
                    self.latticeSize / ((float(
                        self.idealBasalStemCellsVol) - float(basalStemVolume))**2.0 / 3.0 + self.latticeSize))) / 3.0
            for x in xrange(13, self.execConfig.xDimension, 20):
                swaps = 0
                layers = 0
                cells_in_order = []
                for y in xrange(3, self.execConfig.yDimension, 7):
                    #Gives the mode of a cell ID in a 5x3 pixels rectangle
                    mode_of_cellIDs = []
                    for width in xrange(0, 2, 1):
                        for height in xrange(0, 2, 1):
                            if self.cellField[x + width, y + height, 0] is not None:
                                mode_of_cellIDs.append(self.cellField[x + width, y + height, 0].id)
                    #If mode ID exists and in not already in cell_in_order list it will be added
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
                    if cells_in_order[layers-1].type == self.UMBRELLA:
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
                    for x in range(firstLayer, len(cells_in_order)-1-lastLayer, 1):
                        if cells_in_order[x].type != self.INTERMEDIATE:
                            layersInBetween -= 1
                    fitness_a = 1.0 / ((1.0 - float(firstLayer)) + (1.0 - float(lastLayer)) + (layers - layersInBetween) +  1.0)
                sumFitness_a.append(fitness_a)
            if len(sumFitness_a) == 0:
                self.optimum.append(0 + 1.0 / 2.0 * fitness_v)
            else:
                fitness_a = sum(sumFitness_a) / len(sumFitness_a)
                self.optimum.append(
                    1.0 / 2.0 * fitness_a + 1.0 / 2.0 * fitness_v)
            if len(self.optimum) == 0:
                fitness = 0
            else:
                fitness = sum(self.optimum) / len(self.optimum)

            fileName="FitnessPlot.dat"
            try:
                import CompuCellSetup
                fileHandle,fullFileName=CompuCellSetup.openFileInSimulationOutputDirectory(fileName,"a")
            except IOError:
                print "Could not open file ", fileName," for writing. Check if you have necessary permissions"

            fileHandle.write("%s " % (float(mcs)/1440.0))
            fileHandle.write("%s " % (fitness))
            fileHandle.write("\n")

            fileHandle.close()

            fileName="FitnessArrangement.dat"
            try:
                import CompuCellSetup
                fileHandle,fullFileName=CompuCellSetup.openFileInSimulationOutputDirectory(fileName,"a")
            except IOError:
                print "Could not open file ", fileName," for writing. Check if you have necessary permissions"

            fileHandle.write("%s " % (float(mcs)/1440.0))
            fileHandle.write("%s " % (fitness_a))
            fileHandle.write("\n")

            fileHandle.close()

            fileName="FitnessVolume.dat"
            try:
                import CompuCellSetup
                fileHandle,fullFileName=CompuCellSetup.openFileInSimulationOutputDirectory(fileName,"a")
            except IOError:
                print "Could not open file ", fileName," for writing. Check if you have necessary permissions"

            fileHandle.write("%s " % (float(mcs)/1440.0))
            fileHandle.write("%s " % (fitness_v))
            fileHandle.write("\n")

            fileHandle.close()

            del self.optimum[:]


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

