from Core.ExecConfig import ExecConfig
from ModuroModel.CMInDae import CMInDae

class CMInDae2(CMInDae):

    def __init__(self, sim, simthread):
        CMInDae.__init__(self, sim, simthread)

    def _createExecConfig(self, srcDir):
        return ExecConfig(srcDir=srcDir,
                          xLength=500, yLength=100, zLength=0, voxelDensity=1,
                          MCSperDay=500,
                          fluctuationAmplitude=10.0)
