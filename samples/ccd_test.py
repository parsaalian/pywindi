from windi.winclient import Winclient
from windi.windevice import Windevice
import time

client = Winclient()
ccd = client.get_device_by_name('SBIG CCD')
#f = open('time_estimate.txt', 'a+')
#t = int(input())
for t in range(5, 60, 5):
    print(t)
    start = time.time()
    ccd.take_image(t)
    print(str(t) + ': ' + str(time.time() - start) + ',\n')
#f.close()
client.disconnectServer()
