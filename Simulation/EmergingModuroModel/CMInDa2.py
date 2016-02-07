from Core.ExecConfig import ExecConfig
from ModuroModel.CMInDa import CMInDa

class CMInDa2(CMInDa):

    def __init__(self, sim, simthread, srcDir):
        CMInDa.__init__(self, sim, simthread, srcDir)

    def _createExecConfig(self, srcDir):
        return ExecConfig(srcDir=srcDir,
                          xLength=200, yLength=100, zLength=0, voxelDensity=1,
                          MCSperDay=500,
                          fluctuationAmplitude=10.0)
