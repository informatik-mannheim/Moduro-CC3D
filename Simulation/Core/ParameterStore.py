class ParameterStore(object):
    """
    Saves and restores parameter for simulations.
    """

    def __init__(self):
        self.params = []

    def setParameter(self, clazz, name, value):
        """
        Sets a parameter.
        :param clazz: Class this parameter belongs to.
        :param name: Name of the parameter.
        :param value: Value of the parameter.
        :return:
        """
        # clazz_ = clazz.__class__.__name__ # Name of the calling class.
        # self.params[clazz] = "Foo"
        return None

    def getParameters(self, clazz):
        """
        Get a list of all parameters for the specified simulation class.
        Parameters can be loaded before.
        :param clazz:
        :return:
        """
        return []

    def writeParameterfile(self, filename):
        """
        Writes all parameters to a file.
        :param filename:
        :return:
        """
        try:
            import CompuCellSetup
            fileHandle, fullFileName = CompuCellSetup.openFileInSimulationOutputDirectory(filename, "a")
        except IOError:
            print "Could not open file ", filename, \
                " for writing. Check if you have necessary permissions."
        fileHandle.write("startTime: %s \n" % "2014-12-11 15:12:32.063000")
        fileHandle.write("SEED: %s \n" % "100578200")
        fileHandle.write("\n")
        fileHandle.close()

    def readParameterfile(self, filename):
        """
        Reads parameters from a file.
        :param filename:
        :return:
        """
        return None