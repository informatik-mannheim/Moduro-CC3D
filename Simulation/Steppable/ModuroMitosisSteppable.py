__author__ = 'markus'
import random
from PySteppablesExamples import MitosisSteppableBase

class ModuroMitosisSteppable(MitosisSteppableBase):
    def __init__(self, simulator, execConfig, model, _frequency=1):
        MitosisSteppableBase.__init__(self, simulator, _frequency)
        self.execConfig = execConfig
        self.model = model

    def step(self, mcs):
        if not self.execConfig.interuptMCS(mcs):
            self.moduroStep(mcs) # better: not MCS but time!

    # Abstract method:
    def moduroStep(self, mcs):
        return None
