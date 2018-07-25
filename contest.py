from windi.context import Context
from windi.device_handler import DeviceHandler
import time

context = Context()
ccd = context.get_device_by_name('SBIG CCD')
ccd.take_image(0.5)

context.disconnectServer()
