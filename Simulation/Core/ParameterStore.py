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
        return None

    def readParameterfile(self, filename):
        """
        Reads parameters from a file.
        :param filename:
        :return:
        """
        return None