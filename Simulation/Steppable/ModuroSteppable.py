__author__ = 'markus'
from PySteppables import SteppableBasePy

class ModuroSteppable(SteppableBasePy):
    def __init__(self, simulator, execConfig, model, _frequency=1):
        SteppableBasePy.__init__(self, simulator, _frequency)
        self.execConfig = execConfig
        self.model = model

    def step(self, mcs):
        if not self.execConfig.interuptMCS(mcs):
            self.moduroStep(mcs) # better: not MCS but time!

    # Abstract method:
    def moduroStep(self, mcs):
        return None
