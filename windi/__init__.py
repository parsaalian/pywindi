'''import PyIndi
from subprocess import Popen
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


# Initiate the camera for stream.
#
def initiateStreamMode(self, agent):
    # We should inform the indi server that we want to receive the "CCD1" blob from this device.
    agent.setProperty("ccd video stream", {0: True, 1: False})
    self.setBLOBMode(PyIndi.B_ALSO, self.deviceName, "CCD1")
'''
