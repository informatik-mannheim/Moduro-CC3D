class ParameterStore(object):
    """
    Saves and restores parameter for simulations.
    """

    def __init__(self):
        self.params = []
        self.__fileHandle = None
        self.__fullFileName = None

    def setParameter(self, clazz, name, value):
        """
        Sets a parameter.
        :param clazz: Class this parameter belongs to.
        :param name: Name of the parameter.
        :param value: Value of the parameter.
        :return:
        """
        self.params.append([clazz, name, value])

    def getParameters(self, clazz):
        """
        Get a list of all parameters for the specified simulation class.
        Parameters can be loaded before.
        :param clazz:
        :return:
        """
        parameters = (x for x in self.params if x[0] == clazz)
        return parameters

    def __openParameterfile(self, filename):
        """
        Writes all parameters to a file.
        :param filename:
        :return:
        """
        #TODO: change from pure text file to xml?
        try:
            import CompuCellSetup
            self.__fileHandle, self.__fullFileName = CompuCellSetup.openFileInSimulationOutputDirectory(filename, "a")
        except IOError:
            print "Could not open file ", filename, \
                " for writing. Check if you have necessary permissions."

    def saveParameterfile(self, filename):
        self.__openParameterfile(filename)
        self.__fileHandle.write("startTime: %s \n" % "2014-12-11 15:12:32.063000")
        self.__fileHandle.write("SEED: %s \n" % "100578200")
        for x in self.params:
            self.__fileHandle.write("In '{0}', '{1}' is set to: '{2}' \n".format(x[0], x[1], x[2]))
        self.__fileHandle.close()

    def readParameterfile(self, filename):
        """
        Reads parameters from a file.
        :param filename:
        :return:
        """
        return None