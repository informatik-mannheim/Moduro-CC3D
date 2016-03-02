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
__status__ = "Production"

import random
from PySteppablesExamples import MitosisSteppableBase

class ModuroMitosisSteppable(MitosisSteppableBase):
    def __init__(self, simulator, model, _frequency=1):
        MitosisSteppableBase.__init__(self, simulator, _frequency)
        self.model = model
        self.execConfig = model.execConfig

    def step(self, mcs):
        if not self.execConfig.interuptMCS(mcs):
            self.moduroStep(mcs) # better: not MCS but time!

    # Abstract method:
    def moduroStep(self, mcs):
        return None
