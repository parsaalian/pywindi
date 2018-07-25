import PyIndi
from windi.drivers import CCD
from threading import Event, Lock, Semaphore
import sys

class EventManager:
    event_dict = {}
    lock = Lock()

    def __init__(self, timeout):
        self.timeout = timeout

    def send(self, key):
        self.lock.acquire()
        if not key in self.event_dict:
            e = Event()
            self.event_dict[key] = e
        else:
            e = self.event_dict[key]
        self.lock.release()
        e.set()
    def wait(self, key):
        self.lock.acquire()
        if not key in self.event_dict:
            e = Event()
            self.event_dict[key] = e
        else:
            e = self.event_dict[key]
        self.lock.release()
        e.wait(self.timeout)


class Context(PyIndi.BaseClient):
    device_wait = EventManager(10)
    property_wait = EventManager(10)
    blob_semaphore = Semaphore(0)

    def __init__(self, host='localhost', port=7624):
        super(Context, self).__init__()
        self.setServer(host, port)
        if not self.connectServer():
            print('No server running on ' + host + ':' + str(port) + '.')
            sys.exit(1)


    def newDevice(self, d):
        self.device_wait.send(d.getDeviceName())

    def newProperty(self, p):
        self.property_wait.send(p.getDeviceName() + '::' + p.getName())

    def removeProperty(self, p):
        pass
    def newBLOB(self, bp):
        self.blob_semaphore.release()
    def newSwitch(self, svp):
        pass
    def newNumber(self, nvp):
        if nvp.name == 'CCD_TEMPERATURE':
            print('tempraure: ' + str(nvp[0].value))
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

    # Returns the device with name given.
    #
    # @param device_name {String} - the name of the device for connection.
    def get_device_by_name(self, device_name):
        self.device_wait.wait(device_name)
        indi_device = self.getDevice(device_name)
        if str(indi_device.getDriverName()).lower().find('ccd'):
            return CCD(self, indi_device)
        raise Exception('Unknown driver.')

    def wait_for_property(self, device_name, property_name):
        self.property_wait.wait(device_name + '::' + property_name)
