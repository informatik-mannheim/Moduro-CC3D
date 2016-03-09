# Example for Simulation.

# Important to have it here. Otherwise error. CC3D uses a special module loader
# that cannot directly instantiate classes. (Wish I knew more on Python)
import sys
from os import environ

import CompuCellSetup

sys.path.append(environ["PYTHON_MODULE_PATH"])
sim, simthread = CompuCellSetup.getCoreSimulationObjects()

# Now load the model to simulate!
import Settings.DirectoryPath
from Test.Scalability.VerifyGrowthT500D1 import VerifyGrowthT500D1
model = VerifyGrowthT500D1(sim, simthread, Settings.DirectoryPath.getSrcPath())
from Test.Scalability.VerifyGrowthT1000D1 import VerifyGrowthT1000D1
#model = VerifyGrowthT1000D1(sim, simthread, Settings.DirectoryPath.getSrcPath())
#model = VerifyGrowthT2000D1(sim, simthread, Settings.DirectoryPath.getSrcPath())
#model = VerifyGrowthT1000D2(sim, simthread, Settings.DirectoryPath.getSrcPath())
# srcDir is required to know where CellsInit.piff is.

