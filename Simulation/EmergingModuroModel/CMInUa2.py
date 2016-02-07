from Core.ExecConfig import ExecConfig
from ModuroModel.CMInUa import CMInUa

class CMInUa2(CMInUa):

    def __init__(self, sim, simthread, srcDir):
        CMInUa.__init__(self, sim, simthread, srcDir)

    def _createExecConfig(self, srcDir):
        return ExecConfig(srcDir=srcDir,
                          xLength=800, yLength=100, zLength=0, voxelDensity=0.8,
                          MCSperDay=500,
                          fluctuationAmplitude=10.0)
