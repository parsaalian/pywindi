import PyIndi
from windi.windrivers import *
from windi.event import *
from threading import Semaphore
import sys

class Winclient(PyIndi.BaseClient):
    devices_list = {}

    device_wait = EventManager(10)
    property_wait = EventManager(10)
    temprature_wait = EventManager(10)
    blob_semaphore = Semaphore(0)

    def __init__(self, host='localhost', port=7624):
        super(Winclient, self).__init__()
        # Connects to the given server.
        self.setServer(host, port)
        if not self.connectServer():
            print('No server running on ' + host + ':' + str(port) + '.')
            sys.exit(1)


    ################################# INDI BUILT IN FUNCTIONS #################################
    def newDevice(self, d):
        self.device_wait.send(d.getDeviceName())

    def newProperty(self, p):
        
        self.property_wait.send(p.getDeviceName() + '::' + p.getName())

    def removeProperty(self, p):
        pass

    def newBLOB(self, bp):
        #print('NEW BLOB :: ', bp)
        self.blob_semaphore.release()

    def newSwitch(self, svp):
        pass

    # prints the temprature of a ccd everytime it is changed.
    def newNumber(self, nvp):
        pass
        '''if nvp.name == 'CCD_TEMPERATURE':
            print('tempraure: ' + str(nvp[0].value))'''

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
    def get_device_by_name(self, device_name, **kwargs):
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
