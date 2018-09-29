from pywindi.windevice import Windevice
import PyIndi
import os
import io
import time
import traceback

class SBIG_CCD(Windevice):
    def __init__(self, winclient, indi_device):
        super().__init__(winclient, indi_device)
        self.config = {'image_directory': None}


    def configure(self, **kwargs):
        for name, conf in kwargs.items():
            self.config[name] = conf
        for dir in self.config:
            if not os.path.exists(self.config[dir]):
                os.makedirs(self.config[dir])


    def set_binning(self, bin_x, bin_y):
        self.set_property('CCD_BINNING', [bin_x, bin_y])


    def set_frame_type(self, type):
        types = {'light': 0, 'bias': 1, 'dark': 2, 'flat': 3}
        enum_type = types[type]
        set_value = [enum_type == 0, enum_type == 1, enum_type == 2, enum_type == 3]
        self.set_property('CCD_FRAME_TYPE', set_value)


    def set_ccd_cooler(self, **kwargs):
        properties_list = [cooler_on, cooler_off]
        self.set_global_property(CCD_COOLER, properties_list, **kwargs)


    def set_temperature(self, temperature):
        self.set_ccd_cooler(cooler_on=True)
        self.set_property('CCD_TEMPERATURE', [temperature])
        self._winclient.conditional_wait.wait('CCD_TEMPERATURE', lambda x : (x <= temperature + 0.5) and (x >= temperature - 0.5), None)
        print('temperature is set')


    def take_image(self, exposure_time):
        tick = time.time()
        self._winclient.wait_for_property('SBIG CCD', 'CCD1')
        self._winclient.setBLOBMode(1, self._device.getDeviceName(), None)
        self.set_property('CCD_EXPOSURE', [exposure_time])
        print('Capturing image...')
        # Get image data
        try:
            img = self._winclient.blob_queue['SBIG CCD'].pop()[1]
        except Exception as e:
            traceback.print_exc()
            print(self._device.getDeviceName(), 'disconnected.\nCouldn\'t capture image.')
            return
        # Write image data to BytesIO buffer
        blobfile = io.BytesIO(img.getblobdata())
        # Get fits directory
        cwd = self.config['image_directory']
        # Create datetime for file name
        time_str = time.strftime("%Y%m%d%H%M%S")
        # Append date time to file name]
        print (cwd)
        filename = cwd + time_str + ".fits"

        # Open a file and save buffer to disk
        with open(filename, "wb") as f:
            f.write(blobfile.getvalue())

        print('Image saved in', self.config['image_directory'])
        return filename


class V4L2_CCD(Windevice):
    def __init__(self, winclient, indi_device, **kwargs):
        super().__init__(winclient, indi_device, **kwargs)


    def initiate_stream_mode(self):
        # We should inform the indi server that we want to receive the "CCD1" blob from this device.
        self.set_property("CCD_VIDEO_STREAM", [True, False])
        self._winclient.setBLOBMode(PyIndi.B_ALSO, self._device.getDeviceName(), "CCD1")
