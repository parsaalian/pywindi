from windi.windevice import Windevice
import PyIndi
import os
import io
import time

class SBIG_CCD(Windevice):
    config = {'image_directory': '/home/dimm/Desktop/images/'}

    def __init__(self, winclient, indi_device, **kwargs):
        super().__init__(winclient, indi_device)
        self._winclient.setBLOBMode(1, self._device.getDeviceName(), None)
        # Make config directories.
        for dir in self.config:
            if not os.path.exists(self.config[dir]):
                os.makedirs(self.config[dir])


    def configure(self, **kwargs):
        for name, conf in kwargs.items():
            self.config[name] = conf


    def set_temperature(self, temperature):
        self.set_property('CCD_TEMPERATURE', [temperature])


    def take_image(self, exposure_time):
        self.set_property('CCD_EXPOSURE', [exposure_time])
        self._winclient.blob_semaphore.acquire()
        # Get image data
        img = self.get_property('CCD1', True, 0)
        # Write image data to BytesIO buffer
        blobfile = io.BytesIO(img.getblobdata())
        # Get fits directory
        cwd = self.config['image_directory']

        # Create datetime for file name
        time_str = time.strftime("%Y%m%d%H%M%S")
        # Append date time to file name
        filename = cwd + "r" + "_" + time_str + ".fits"

        # Open a file and save buffer to disk
        with open(filename, "wb") as f:
            f.write(blobfile.getvalue())


class V4L2_CCD(Windevice):
    def __init__(self, winclient, indi_device, **kwargs):
        super().__init__(winclient, indi_device, **kwargs)


    def initiate_stream_mode(self):
        # We should inform the indi server that we want to receive the "CCD1" blob from this device.
        self.set_property("CCD_VIDEO_STREAM", [True, False])
        self._winclient.setBLOBMode(PyIndi.B_ALSO, self._device.getDeviceName(), "CCD1")
