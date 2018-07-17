import PyIndi
from time import sleep
from windi._indiclient import IndiClient

class Controller(IndiClient):
    def __init__(self):
        super(Controller, self).__init__()

    def __setServer(self, ip='localhost', port=7624):
        self.setServer(ip, port)

    def connectClientToServer(self, deviceName, ip='localhost', port=7624):
        self.__setServer(ip, port)
        device = None
        device_connect = None

        device = self.getDevice(deviceName.upper())
        for i in range(10):
            if device is not None:
                break
            sleep(0.5)
            device = self.getDevice(deviceName.upper())
        if device is None:
            self.sendException('Device not found.')

        device_connect = device.getSwicth("CONNECTION")
        for i in range(10):
            if device.isConnected():
                break
            device_connect = self.setSwitch(device_connect, PyIndi.ISS_OFF, PyIndi.ISS_ON)
            self.sendNewSwitch(device_connect)

        if not(device.isConnected()):
            self.sendException('Can not connect the device.')

    def setSwitch(self, switch, *args):
        for i in range(len(args)):
            switch[i].s = args[i]
        return switch

    def setText(self, text, *args):
        for i in range(len(args)):
            text[i].text = args[i]
        return text

    def setNumber(self, number, *args):
        for i in range(len(args)):
            number[i].value = args[i]
        return number

    def sendException(self, exceptionMessage):
        raise Exception(exceptionMessage)
