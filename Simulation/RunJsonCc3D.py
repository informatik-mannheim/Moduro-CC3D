
import sys
from os import environ

import CompuCellSetup
sys.path.append(environ["PYTHON_MODULE_PATH"])

sim, simthread = CompuCellSetup.getCoreSimulationObjects()

# Now load the model to simulate!
from ModuroModel.Sd.JsonBasedModelDa import JsonBasedModelDa
model = JsonBasedModelDa(sim, simthread)
print "Model initialized. Running simulation...."
model._run()

