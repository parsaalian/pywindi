import PyIndi
from subprocess import Popen
from windi._indiclient import IndiClient
import sys, time

# Start an indi server
#
# @param serverType {String} - type of server to run. e.g. "v4l2 ccd" -> "indi_v4l2_ccd"
def startServer(serverType):
    serverType = 'indi_' + serverType.replace(' ', '_').lower()
    Popen('indiserver\ ' + serverType, shell=True)


# Kill the server started in start server function (or in the command line)
#
# @param port {number} - port of server to terminate. default value is 7624.
def killServer(port=7624):
    Popen('fuser -k\ ' + str(port) + '/tcp || true', shell=True)

# Controller for all of actions with PyIndi, such as connecting to server, changing properties and ...
#
class Controller(IndiClient):
    def __init__(self):
        super(Controller, self).__init__()

    # Check if indi server is running or not
    #
    # @param deviceName {String} - the name of the connecting decive to suggest if no server was running. e.g. v4l2 ccd
    def __serverConnectedCheck(self, deviceName):
        if not self.connectServer():
             print("No indiserver running on " + self.getHost() + ":" + str(self.getPort()) + " - Try to run:")
             print("    indiserver indi_" + deviceName.replace(' ', '_').lower())
             sys.exit(1)

    # Trying to connect given device for one timeself.
    #
    # @param deviceName {String} - the name of the connecting device.
    # @param host {String} - the name of host which server is running on.
    # @param port {Number} - the port of the host which server is running on.
    def _oneStepConnect(self, deviceName, host='localhost', port=7624):
        self.setServer(host, port)
        self.__serverConnectedCheck(deviceName)

        deviceName = deviceName.upper()
        device = None
        deviceConnect = None

        device = self.getDevice(deviceName)
        while device is None:
            time.sleep(0.5)
            device = self.getDevice(deviceName)

        self.device = device

        deviceConnect = device.getSwitch("CONNECTION")
        while deviceConnect is None:
            time.sleep(0.5)
            deviceConnect = device.getSwitch("CONNECTION")

        for i in range(2):
            if device.isConnected():
                break
            time.sleep(0.5)
            deviceConnect[0].s = PyIndi.ISS_ON
            deviceConnect[1].s = PyIndi.ISS_OFF
            self.sendNewSwitch(deviceConnect)

        self.deviceConnected = device.isConnected()
        return device.isConnected()

    # Change the given property of device.
    #
    # @param propertyName {String} - the name of the property to change.
    # @param type {String} - type of the changing property: 1. switch - 2. text - 3. number - 4. blob
    # @param *args {Boolean|String|Number|Blob} - new values for the property depends on type. Boolean for switch, Text for text and Number for number
    def setProperty(self, propertName, type, *args):
        if type == 'switch':
            self.__setSwitch(propertName, *args)
        elif type == 'text':
            self.__setText(propertName, *args)
        elif type == 'number':
            self.__setNumber(propertName, *args)
        elif type == 'blob':
            self.__setBlob(propertName, *args)
        else:
            raise Exception('Unavailable type of property.')

    # Get the value of the given property.
    #
    # @param propertName {String} - the name of the property to get.
    # @param type {String} - type of the changing property: 1. switch - 2. text - 3. number - 4. blob.
    # @param index {Number} - the index of the sub property.
    def getProperty(self, propertyName, type, index):
        ret = None
        if type == 'switch':
            return self.__getSwitch(propertyName, index)
        elif type == 'text':
            return self.__getText(propertyName, index)
        elif type == 'number':
            return self.__getNumber(propertyName, index)
        elif type == 'blob':
            return self.__getBLOB(propertyName, index)
        else:
            raise Exception('Unavailable type of property.')

    #######################################################
    ######################  setters  ######################
    #######################################################
    # Set values for switch properties.
    #
    # @param propertyName {String} - name of property to change, which is a switch.
    # @param *args {Boolean} - new values for properties.
    def __setSwitch(self, propertyName, *args):
        switch = self.device.getSwitch(propertyName.replace(' ', '_').upper())
        for i in range(len(args)):
            switch[i].s = PyIndi.ISS_ON if args[i] == True else PyIndi.ISS_OFF
        self.sendNewSwitch(switch)

    # Set values for text properties.
    #
    # @param propertyName {String} - name of property to change, which is a text.
    # @param *args {String} - new values for properties.
    def __setText(self, propertyName, *args):
        text = self.device.getSwitch(propertyName.replace(' ', '_').upper())
        for i in range(len(args)):
            text[i].text = args[i]
        self.sendNewText(text)

    # Set values for number properties.
    #
    # @param propertyName {String} - name of property to change, which is a switch.
    # @param *args {Number} - new values for properties.
    def __setNumber(self, propertyName, *args):
        number = self.device.getSwitch(propertyName.replace(' ', '_').upper())
        for i in range(len(args)):
            number[i].value = args[i]
        self.sendNewNumber(number)

    ###########################################################################

    #######################################################
    ######################  getters  ######################
    #######################################################
    # Get the value of switch propeties.
    #
    # @param propertyName {String} - name of property to get, which is a switch.
    # @para, index {Number} - the index of the sub property.
    def __getSwitch(self, propertyName, index):
        return self.device(propertyName.replace(' ', '_').upper())[index].s

    # Get the value of text propeties.
    #
    # @param propertyName {String} - name of property to get, which is a text.
    # @para, index {Number} - the index of the sub property.
    def __getText(self, propertyName, index):
        return self.device(propertyName.replace(' ', '_').upper())[index].text

    # Get the value of number propeties.
    #
    # @param propertyName {String} - name of property to get, which is a number.
    # @para, index {Number} - the index of the sub property.
    def __getNumber(self, propertyName, index):
        return self.device(propertyName.replace(' ', '_').upper())[index].values

    # Get the value of blob propeties.
    #
    # @param propertyName {String} - name of property to get, which is a blob.
    # @para, index {Number} - the index of the sub property.
    def __getBLOB(self, propertyName, index):
        return self.device(propertyName.replace(' ', '_').upper())[index].blob

    ############################################################################


def createNewController(deviceName):
    numCtrls = 10
    controllers = [Controller() for i in range(numCtrls)]
    for i in range(numCtrls):
        connected = controllers[i]._oneStepConnect(deviceName)
        if connected:
            return controllers[i]
        print("Test " + str(i + 1) + " failed.")
    print("No device is connected to the system. Please connect and try again.")
    sys.exit(1)
