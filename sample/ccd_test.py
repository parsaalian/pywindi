from pywindi.winclient import Winclient
from pywindi.windevice import Windevice
import time

client = Winclient()
ccd = client.get_device('SBIG CCD')
#f = open('time_estimate.txt', 'a+')
#t = int(input())
#f.close()
client.disconnectServer()
