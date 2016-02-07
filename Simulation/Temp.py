# Example for Simulation.

# Important to have it here. Otherwise error. CC3D uses a special module loader
# that cannot directly instantiate classes. (Wish I knew more on Python)
import sys
from os import environ

import CompuCellSetup

sys.path.append(environ["PYTHON_MODULE_PATH"])
sim, simthread = CompuCellSetup.getCoreSimulationObjects()

# Now load the model to simulate!
from EmergingModuroModel.CMInDa2 import CMInDa2
model = CMInDa2(sim, simthread,"c:\Users\Markus\Local-Docs\src\cc3d\Moduro-CC3D")
# srcDir is required to know where CellsInit.piff is.
