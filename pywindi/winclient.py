import PyIndi
from pywindi.windrivers import *
from pywindi.utils import *
import sys
import time

class Winclient(PyIndi.BaseClient):
    """This class is the basic client of pywindi package. For every
    system that is connecting to the server, a client should be initiated.
    If multiple systems are connecting to the server, a client should be
    created for each one of them.

    Also multiple devices can be connected to a winclient, but the name of
    the devices should be exclusive, or the client will return the first
    connected device on each call (for inclusive device names), and the other
    devices will be ignored (this issue is in indi, not pywindi).

    :param host: the address of the host to connect. The default value is 'localhost'
    :param port: the port of the host to connect. The default value is 7624 which is
                 the default reserved port for indi.
    """

    def __init__(self, host='localhost', port=7624):
        super(Winclient, self).__init__()
        #: a dictionary with devices. The keys are devices names and the valus are
        #: pywindi objects.
        self.devices_list = {}

        #: a dictionary which the keys are devices names and the values are objects
        #: of type utils.Queue. In this data structure, the received blobs of each
        #: device is saved in the queue until it is called.
        self.blob_queue = {}

        #: event managers for devices and properties. If they are received from the
        #: system, the respected event of them will be set in the event manager.
        self.device_wait = EventManager(600)
        self.property_wait = EventManager(600)
        self.conditional_wait = EventManager(600)

        self.host = host
        #: connects to the given server.
        self.setServer(host, port)
        if not self.connectServer():
            print('No server running on ' + host + ':' + str(port) + '.')
            sys.exit(1)


    ################################# INDI BUILT IN FUNCTIONS #################################
    def newDevice(self, d):
        print('New Device ::', d.getDeviceName())
        #: tells the device event manager that the device has arrived.
        self.device_wait.send(d.getDeviceName())

    def newProperty(self, p):
        #: initiate the queue in blob_queue, if the blob property of device
        #: has arrived.
        if p.getName() == 'CCD1':
            self.blob_queue[p.getDeviceName()] = Queue(200)

        #: tells the property event manager that property of specified device
        #: has arrived.
        self.property_wait.send(p.getDeviceName() + '::' + p.getName())

    def removeProperty(self, p):
        pass

    def newBLOB(self, bp):
        #: adds the new blob to its queue.
        self.blob_queue[bp.bvp.device].push([time, bp])

    def newSwitch(self, svp):
        pass

    def newNumber(self, nvp):
        if nvp.name == 'CCD_TEMPERATURE':
            print('temperature: ', round(nvp[0].value, 3))
            self.conditional_wait.send('CCD_TEMPERATURE', nvp[0].value)

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
        """This method will return the device with the given name.

        :param device_name: the name of the device for connection.
        """

        #: wait for device to connect.
        self.device_wait.wait(device_name)

        #: gets the device with its name from client (self).
        indi_device = self.getDevice(device_name)

        #: waits for the driver info property. Before the arrival of this property,
        #: some of the properties can not be changed, because the system does not
        #: recognize them.
        self.wait_for_property(indi_device.getDeviceName(), 'DRIVER_INFO')

        #: if the device with this name is already connected to the system, it
        #: returns it.
        if device_name in self.devices_list:
            return self.devices_list[device_name]

        #: cases for device type.
        # TODO: add more devices to the drivers.
        if indi_device.getDriverName() == 'SBIG CCD':
            self.devices_list[device_name] = SBIG_CCD(self, indi_device, **kwargs)
            return self.devices_list[device_name]
        elif indi_device.getDriverName() == 'V4L2 CCD':
            self.devices_list[device_name] = V4L2_CCD(self, indi_device, **kwargs)
            return self.devices_list[device_name]

        #: in case of unknown device name for the package.
        raise Exception('Unknown driver.')


    def wait_for_property(self, device_name, property_name):
        """Waits for recognition of a property from an specified device.

        :param device_name: the name of the device which property is in.
        :param property_name: the name of the property in device.
        """
        self.property_wait.wait(device_name + '::' + property_name)
