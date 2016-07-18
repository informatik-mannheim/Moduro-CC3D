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

__author__ = "Julian Debatin"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "juliandebatin@gmail.com"
__status__ = "Production"

from EmergingModuroModel.Spa.SpaSdbPcdiInUa import SpaSdbPcdiInUa


class SpaSdbPcdiInDa(SpaSdbPcdiInUa):
    def __init__(self, sim, simthread):
        SpaSdbPcdiInUa.__init__(self, sim, simthread)

    def _initModel(self):
        self.name = "SpaSdbPcdiInDa"
        self.adhFactor = 0.25
        self.cellTypes = self._createCellTypes()
        self.energyMatrix = self._createEnergyMatrix()
        self._run() # Must be the last statement.


    def _createEnergyMatrix(self):
        energyMatrix = [[0, 14, 14, 14, 14, 4],
                        [0, -1, 1, 3, 12, 12],
                        [0, 0, 6, 4, 8, 14],
                        [0, 0, 0, 5, 8, 12],
                        [0, 0, 0, 0, 6, 4],
                        [0, 0, 0, 0, 0, 2]]

        return energyMatrix