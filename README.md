#PyWindi

PyWindi Project is a wrapper for PyIndi library that automates many functionalities with a simple interface.
It is a package for python and the commands for terminal will be available in future versions.

## Installation

Use pip (recommended, but not yet)

```
pip3 install windi
```


Alternatively download [a release](https://gitlab.com/parsaalian0/windi/-/archive/master/windi-master.zip), extract it and run

```
python3 setup.py install
```


### Prerequisites

For the above installation to work, you need to have installed from your distribution repositories the following packages: libindi and pyindi-client.

For installing libindi

```
sudo apt-add-repository ppa:mutlaqja/ppa
sudo apt-get update
sudo apt-get install indi-full
sudo apt-get install swig libz3-dev libcfitsio-dev libnova-dev
```

For installing python pyindi-client:

```
pip3 install --user --install-option="--prefix=" pyindi-client
sudo -H pip3 install --system pyindi-client
```

If any errors occurred during the installation, download [pyindi-client release](https://github.com/jochym/pyindi-client/tree/master/pip/pyindi-client), extract it and run

```
python3 setup.py install
```

## Built With

* [libindi](https://github.com/indilib/indi) - The Astronomical Instrumentation Control.
* [pyindi-client](https://github.com/jochym/pyindi-client/tree/master/pip/pyindi-client) - An INDI Client Python API.

## Authors

* **Parsa Alian** - *Initial work* - [parsaalian0](https://gitlab.com/parsaalian0)
* **Emad Salehi** - [emad_salehi](https://gitlab.com/emad_salehi)
* **Seyed Sajad Kahani** - [sskahani](https://gitlab.com/sskahani)

## License

This project is free under the GPL License.

##Programing with PyWindi
####1. Connect to indiserver
To use pywindi and connect indi devices you should launch an *indiserver* on your localhost or on another device in your
 network. To do this, you must have the indi device name you intend to connect to. For example if you want connect a SBIG
  CCD you should run this command in terminal.

    indiserver indi_sbig_ccd
If you want connect multiple device you can try this for SBIG CCD and V4L2 CCD.
    
    indiserver indi_sbig_ccd indi_v4l2_ccd
####2. Connect to a Winclient
To connect to a indi client you should first import *Winclient* from *pywindi.winclient* and next define a client to
 connect to device.

You can connect to a client in your network with Winclient and you must have their IP. Also you can set the port of client
 with Winclient and it have default value 7624. (It reserve fot indi devices.)

    from pywindi.winclient import Winclient
    
    network_client = Winclient('192.168.150.72')
    local_client = Winclient()
    
####3. Connect to device
to connect *local_client* in section2 to a V4L2 CCD or SBIG CCD device you must add the code bellow.

    v4l2_device0 = local_client.get_device("V4L2 CCD")
    v4l2_device1 = local_client.get_device("V4L2 CCD", DEVICE_PORT=['/dev/video1'])
    sbig_device = local_client.get_device("SBIG CCD")
    
And next you can do what you want with these defined devices.

####4. Properties
To see properties of devices you can run **test_indiclient.py** code in *sample* directory after doing section1 (connect to indiserver).

test_indiclient.py:

    import sys
    import time
    import logging
    import PyIndi
    
    def strISState(s):
        if (s == PyIndi.ISS_OFF):
            return "Off"
        else:
            return "On"
    
    def strIPState(s):
        if (s == PyIndi.IPS_IDLE):
            return "Idle"
        elif (s == PyIndi.IPS_OK):
            return "Ok"
        elif (s == PyIndi.IPS_BUSY):
            return "Busy"
        elif (s == PyIndi.IPS_ALERT):
            return "Alert"
    
    class IndiClient(PyIndi.BaseClient):
    #class IndiClient(indiclientpython.BaseClient):
    def __init__(self):
        super(IndiClient, self).__init__()
        self.logger = logging.getLogger('PyQtIndi.IndiClient')
        self.logger.info('creating an instance of PyQtIndi.IndiClient')
    def newDevice(self, d):
        self.logger.info("new device " + d.getDeviceName())
        #self.logger.info("new device ")
    def newProperty(self, p):
        self.logger.info("new property "+ p.getName() + " for device "+ p.getDeviceName())
        #self.logger.info("new property ")
    def removeProperty(self, p):
        self.logger.info("remove property "+ p.getName() + " for device "+ p.getDeviceName())
    def newBLOB(self, bp):
        self.logger.info("new BLOB "+ bp.name.decode())
    def newSwitch(self, svp):
        self.logger.info ("new Switch "+ svp.name.decode() + " for device "+ svp.device.decode())
    def newNumber(self, nvp):
        pass
    def newText(self, tvp):
        self.logger.info("new Text "+ tvp.name.decode() + " for device "+ tvp.device.decode())
    def newLight(self, lvp):
        self.logger.info("new Light "+ lvp.name.decode() + " for device "+ lvp.device.decode())
    def newMessage(self, d, m):
        self.logger.info("new Message "+ d.messageQueue(m).decode())
    def serverConnected(self):
        print("Server connected ("+self.getHost()+":"+str(self.getPort())+")")
    def serverDisconnected(self, code):
        self.logger.info("Server disconnected (exit code = "+str(code)+","+str(self.getHost())+":"+str(self.getPort())+")")

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    
    indiclient=IndiClient()
    
    indiclient.setServer("localhost",7624)
    
    print("Connecting and waiting 2secs")
    if (not(indiclient.connectServer())):
         print("No indiserver running on "+indiclient.getHost()+":"+str(indiclient.getPort())+" - Try to run")
         print("  indiserver indi_v4l2_ccd")
         sys.exit(1)
    time.sleep(1)
    
    print("List of devices")
    dl=indiclient.getDevices()
    for dev in dl:
        print(dev.getDeviceName())
    
    print("List of Device Properties")
    for d in dl:
        print("-- "+d.getDeviceName())
        lp=d.getProperties()
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
                    print("       "+t.name+"("+t.label+")= "+strISState(t.s))
            elif p.getType()==PyIndi.INDI_LIGHT:
                tpy=p.getLight()
                for t in tpy:
                    print("       "+t.name+"("+t.label+")= "+strIPState(t.s))
            elif p.getType()==PyIndi.INDI_BLOB:
                tpy=p.getBLOB()
                for t in tpy:
                    print("       "+t.name+"("+t.label+")= <blob "+str(t.size)+" bytes>")
    
    print("Disconnecting")
    indiclient.disconnectServer()

####5. Set property
As you saw in the previous section, you have a lot of properties that you can change them. With following code you can
 change what you want. For example, to change *Image Adjustments* of a camera we can do the following after section 3.
        
    v4l2_device0.set_property("Image Adjustments", [20, 150, None, None, None, None, None, None, None, None, None, None])
        
 As you saw *set_property* method takes name of property (As you saw in section 4) and also takes a list to set them. 
 You can test it yourself to set your properties.
####6. Configuration to take image with SBIG CCD
To taking image from a SBIG CCD you must first configure device. For this you have 2 option.
#####6.1. Command line configuration
You can run following command in terminal and configure *directory* and *hosts*.

    ccd_config --directory  "YOUR_DIRECTORY" --hosts ("localhost", 7624)
    
This command make **ccd_base_config.txt** in pywindi directory and we use that to configure our capturing.
#####6.2. Python code configuration
You can import *config* function in you code and use that like following:

    from pywindi.scripts.config import config
    
    config("YOUR_DIRECTORY", ("localhost", 7624))
    
####7. Take image with SBIG CCD
For taking image with SBIG CCD you have 2 option.
#####7.1. Command line capturing
Run following command in your terminal. You must set all of parameters.

    capture --time #EXPOSURE_TIME --temperature #CCD_TEMPERATURE --binning (#BINNING_X, #BINNING_Y) --interval #IMAGES_INTERVAL_TIME --count #NUMBER_OF_IMAGES_TO_TAKE --type #IMAGE_TYPE
for example:

    capture --time 10 --temprature -10 --binning (1.0, 1.0) --interval 5 --count 30 --type light
Captured images will save in directory you cofigured in section 6.

#####7.2. Python code capturing
First you must add the code bellow.

    file = open('ccd_base_config.txt', 'r')
    image_path = file.readline()[:-1]
    addresses = file.readline()[1:-1].replace(' ', '').split(',')
Then you can use *sbig_device* like following.

    sbig_device.configure(image_directory=image_path + str(addresses[0]) + '/')
And finaly you can set your arbitrary properties and take image like bellow.

    sbig_device.set_temperature(#CCD_TEMPERATURE)
    sbig_device.set_frame_type(#TYPE_OF_IMAGE)
    sbig_device.set_binning(#BINNING_X, #BINNING_Y)
    sbig_device.take_image(#EXPOSURE_TIME)
    
Captured images will save in directory you cofigured in section 6.