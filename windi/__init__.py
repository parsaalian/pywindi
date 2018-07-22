import PyIndi
from subprocess import Popen
from windi._indiclient import IndiClient
import sys, time

# Start an indi server
#
# @param serverType {String} - type of server to run. -> e.g. "v4l2 ccd" -> "indi_v4l2_ccd"
def startServer(serverType):
    serverType = 'indi_' + serverType.replace(' ', '_').lower()
    return Popen(['indiserver', serverType])


# Kill the server started in start server function (or in the command line)
#
# @param port {number} - port of server to terminate. default value is 7624.
def killServer(port=7624):
    Popen(['fuser', '-k', str(port) + '/tcp'])


# Controller for all of actions with PyIndi, such as connecting to server, changing properties and ...
#
class Controller(IndiClient):
    def __init__(self):
        super(Controller, self).__init__()
        self.device = None



    # Check if indi server is running or not
    #
    # @param deviceName {String} - the name of the connecting decive to suggest if no server was running. -> e.g. v4l2 ccd
    def __serverConnectedCheck(self, deviceName):
        if not self.connectServer():
             print("No indiserver running on " + self.getHost() + ":" + str(self.getPort()) + " - Try to run:")
             print("    indiserver indi_" + deviceName.replace(' ', '_').lower())
             sys.exit(1)


    # Trying to connect given device for one timeself.
    #
    # @param deviceName {String} - the name of the connecting device. -> e.g. "v4l2 ccd"
    # @param host {String} - the name of host which server is running on. Default value is localhost. -> e.g. "127.0.0.1"
    # @param port {Number} - the port of the host which server is running on. Default value is 7624. -> e.g. 8080
    def _oneStepConnect(self, deviceName, host='localhost', port=7624):
        self.setServer(host, port)
        self.__serverConnectedCheck(deviceName)

        deviceName = deviceName.upper()
        device = None
        deviceConnect = None
        # Tries to connect to device every 0.5 second (time can change).
        device = self.getDevice(deviceName)
        while device is None:
            time.sleep(0.25)
            device = self.getDevice(deviceName)
        # Set the device status if it is found.
        self.deviceName = deviceName
        self.device = device
        # Tries to get the connection switch every 0.5 second (time can change).
        deviceConnect = device.getSwitch("CONNECTION")
        while deviceConnect is None:
            time.sleep(0.25)
            deviceConnect = device.getSwitch("CONNECTION")
        # checks that device is connected for two times.
        for i in range(2):
            if device.isConnected():
                break
            time.sleep(0.25)
            deviceConnect[0].s = PyIndi.ISS_ON
            deviceConnect[1].s = PyIndi.ISS_OFF
            self.sendNewSwitch(deviceConnect)


        self.deviceConnected = device.isConnected()
        time.sleep(0.5)
        return device.isConnected()


    # Initiate the camera for stream.
    #
    def initiateStreamMode(self):
        # We should inform the indi server that we want to receive the "CCD1" blob from this device.
        self.setProperty("ccd video stream", 'switch', True, False)
        self.setBLOBMode(PyIndi.B_ALSO, self.deviceName, "CCD1")

    def strISState(self, s):
        if (s == PyIndi.ISS_OFF):
            return "Off"
        else:
            return "On"

    def strIPState(self, s):
        if (s == PyIndi.IPS_IDLE):
            return "Idle"
        elif (s == PyIndi.IPS_OK):
            return "Ok"
        elif (s == PyIndi.IPS_BUSY):
            return "Busy"
        elif (s == PyIndi.IPS_ALERT):
            return "Alert"


    def printProperties(self):
        print("List of Device Properties")
        print("-- "+self.device.getDeviceName())
        lp = self.device.getProperties()
        for p in lp:
            print("   > "+p.getName())
            if p.getType()==PyIndi.INDI_TEXT:
                tpy=p.getText()
                for t in tpy:
                    print("       "+t.name+"("+t.label+")= "+t.text)
            elif p.getType()==PyIndi.INDI_NUMBER:
                tpy=p.getNumber()
                for t in tpy:
                    print("       "+t.name+"("+t.label+")= "+str(t.value))
            elif p.getType()==PyIndi.INDI_SWITCH:
                tpy=p.getSwitch()
                for t in tpy:
                    print("       "+t.name+"("+t.label+")= "+self.strISState(t.s))
            elif p.getType()==PyIndi.INDI_LIGHT:
                tpy=p.getLight()
                for t in tpy:
                    print("       "+t.name+"("+t.label+")= "+self.strIPState(t.s))
            elif p.getType()==PyIndi.INDI_BLOB:
                tpy=p.getBLOB()
                for t in tpy:
                    print("       "+t.name+"("+t.label+")= <blob "+str(t.size)+" bytes>")

    ############################################################################


# Tries connecting to server for ten times (maximum). Returns the connected device if connected, else exits the programself.
#
# @param deviceName {String} - the name of the connecting decive. e.g. "v4l2 ccd"
def createNewController(deviceName):
    numCtrls = 10
    controllers = [Controller() for i in range(numCtrls)]
    for i in range(numCtrls):
        connected = controllers[i]._oneStepConnect(deviceName)
        if connected:
            print("Device connected.")
            return controllers[i]
    print("No device is connected to the system. Please connect and try again.")
    sys.exit(1)
