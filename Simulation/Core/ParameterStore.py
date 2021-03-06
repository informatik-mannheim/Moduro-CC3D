# Copyright 2016 the original author or authors.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

__author__ = "Angelo Torelli"
__copyright__ = "The authors"
__license__ = "Apache 2"
__email__ = "m.gumbel@hs-mannheim.de"
__status__ = "Production"

import datetime

class ParameterStore(object):
    """
    Saves and restores parameter for simulations.
    """

    def __init__(self):
        self.params = []
        self.objs = []
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

    def addObj(self, obj):
        self.objs.append(obj)


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

    def saveAllObjs(self, filename):
        self.__openParameterfile(filename)
        self.__fileHandle.write("startTime: %s \n" % str(datetime.datetime.now()))
        for obj in self.objs:
            self.__fileHandle.write("\n" + str(obj.__class__.__name__) + ":\n")
            for a in dir(obj):
                if not a.startswith('_') and not callable(getattr(obj, a)) \
                        and a not in ['parameterStore', 'cellTypes', 'execConfig', 'simthread', 'sim']:
                    self.__fileHandle.write(a + ": " + str(getattr(obj, a)) + "\n")
        self.__fileHandle.close()
