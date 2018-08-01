import PyIndi
from pywindi.windrivers import *
from pywindi.tools import *
from threading import Semaphore
import sys
import time

class Winclient(PyIndi.BaseClient):
    devices_list = {}

    blob_queue = {}

    device_wait = EventManager(10)
    property_wait = EventManager(10)

    def __init__(self, host='localhost', port=7624):
        super(Winclient, self).__init__()
        # Connects to the given server.
        self.setServer(host, port)
        if not self.connectServer():
            print('No server running on ' + host + ':' + str(port) + '.')
            sys.exit(1)


    ################################# INDI BUILT IN FUNCTIONS #################################
    def newDevice(self, d):
        print('New Device ::', d.getDeviceName())
        self.device_wait.send(d.getDeviceName())

    def newProperty(self, p):
        if p.getName() == 'CCD1':
            self.blob_queue[p.getDeviceName()] = Queue(200)
        self.property_wait.send(p.getDeviceName() + '::' + p.getName())

    def removeProperty(self, p):
        pass

    def newBLOB(self, bp):
        self.blob_queue[bp.bvp.device].push([time, bp])

    def newSwitch(self, svp):
        pass

    # prints the temprature of a ccd everytime it is changed.
    def newNumber(self, nvp):
        pass
        #if nvp.name == 'CCD_TEMPERATURE':
        #    print('Temprature: ', round(nvp[0].value, 3))

    def newText(self, tvp):
        pass

    def newLight(self, lvp):
        pass

    def newMessage(self, d, m):
        pass

    def serverConnected(self):
        print('Connected to the server.')

    def serverDisconnected(self, code):
        pass
    ###########################################################################################


    # Returns the device with name given.
    #
    # @param device_name {String} - the name of the device for connection.
    def get_device(self, device_name, **kwargs):
        self.device_wait.wait(device_name)
        indi_device = self.getDevice(device_name)
        self.wait_for_property(indi_device.getDeviceName(), 'DRIVER_INFO')
        if device_name in self.devices_list:
            return self.devices_list[device_name]
        if indi_device.getDriverName() == 'SBIG CCD':
            self.devices_list[device_name] = SBIG_CCD(self, indi_device, **kwargs)
            return self.devices_list[device_name]
        elif indi_device.getDriverName() == 'V4L2 CCD':
            self.devices_list[device_name] = V4L2_CCD(self, indi_device, **kwargs)
            return self.devices_list[device_name]

        raise Exception('Unknown driver.')


    # Waits for recognition of a property from an specified device.
    #
    # @param device_name {String} - the name of the device which property is in.
    # @param property_name {String} - the name of the property in device.
    def wait_for_property(self, device_name, property_name):
        self.property_wait.wait(device_name + '::' + property_name)
