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

__author__ = "Markus Gumbel, Angelo Torelli"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Production"

from Core.ExecConfig import ExecConfig
from ModuroModel.PASCMInDa import PASCMInDa

class PASCMInDa2(PASCMInDa):

    def __init__(self, sim, simthread):
        PASCMInDa.__init__(self, sim, simthread)


    def _createExecConfig(self):
        return ExecConfig(xLength=800, yLength=100, zLength=0, voxelDensity=0.8,
                          MCSperDay=500,
                          SEED=124)
