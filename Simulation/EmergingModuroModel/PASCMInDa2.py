from Core.ExecConfig import ExecConfig
from ModuroModel.PASCMInDa import PASCMInDa

class PASCMInDa2(PASCMInDa):

    def __init__(self, sim, simthread, srcDir):
        PASCMInDa.__init__(self, sim, simthread, srcDir)


    def _createExecConfig(self, srcDir):
        return ExecConfig(srcDir=srcDir,
                          xLength=800, yLength=100, zLength=0, voxelDensity=0.8,
                          MCSperDay=500,
                          SEED=124)
