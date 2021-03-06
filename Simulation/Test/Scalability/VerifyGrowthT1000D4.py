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

__author__ = "Markus Gumbel"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Test"

from Core.ExecConfig import ExecConfig
from Test.Scalability.VerifyGrowth import VerifyGrowth


class VerifyGrowthT1000D4(VerifyGrowth):
    def __init__(self, sim, simthread):
        VerifyGrowth.__init__(self, sim, simthread)
        self.name = "VerifyGrowthT1000D2"
        self._initModel()

    def _createExecConfig(self):
        return ExecConfig(simDurationDays=2,
                          xLength=100, yLength=100, zLength=0,
                          voxelDensity=4, MCSperDay=1000)
