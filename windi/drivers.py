from windi.device_handler import DeviceHandler
import os
import io
import time

class CCD(DeviceHandler):
    config = {'imageDirectory': '/home/dimm/Desktop/images/',
              'logsDirectory': '/'}

    def __init__(self, context, indi_device):
        super().__init__(context, indi_device)
        # Make config directories.
        for dir in self.config:
            if not os.path.exists(self.config[dir]):
                os.makedirs(self.config[dir])


    def set_temperature(self, temperature):
        self.setProperty('CCD_TEMPERATURE', [temperature])


    def take_image(self, exposure_time):
        self.setProperty('CCD_EXPOSURE', [exposure_time])
        self._context.setBLOBMode(1, self._device.getDeviceName(), None)
        self._context.blob_semaphore.acquire()
        # get image data
        img = self.getProperty('CCD1', True, 0)
        # write image data to BytesIO buffer
        blobfile = io.BytesIO(img.getblobdata())
        # get fits directory
        cwd = self.config['imageDirectory']

        # create datetime for file name
        time_str = time.strftime("%Y%m%d%H%M%S")
        # append date time to file name
        filename = cwd + "r" + "_" + time_str + ".fits"

        # open a file and save buffer to disk
        with open(filename, "wb") as f:
            f.write(blobfile.getvalue())
