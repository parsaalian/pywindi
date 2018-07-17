import PyIndi
from time import sleep
from windi._indiclient import *

class Controller:
    def __init__(self):
        self.indiclient = _indiclient.IndieClient()

    def __setServer(self, ip='localhost', port=7624):
        self.indiclient.setServer(ip, port)

    def connectClientToServer(self, deviceName, ip='localhost', port=7624):
        self.__setServer(ip, port)
        device = None
        device_connect = None

        device = self.indiclient.getDevice(deviceName.upper())
        for i in range(10):
            if device is not None:
                break
            sleep(0.5)
            device = self.indiclient.getDevice(deviceName.upper())
        if device is None:
            self.expect('Device not found.')

        device_connect = device.getSwicth("CONNECTION")
        for i in range(10):
            if device.isConnected():
                break
            device_connect = self.setSwitch(device_connect, PyIndi.ISS_OFF, PyIndi.ISS_ON)
            self.indiclient.sendNewSwitch(device_connect)

        if not(device.isConnected()):
            self.expect('Could not connect the device.')

    def setSwitch(self, switch, *args):
        for i in range(len(args)):
            switch[i].s = args[i]
        return switch

    def expect(self, exceptionMessage):
        raise Exception(exceptionMessage)
