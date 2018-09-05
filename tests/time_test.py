import time
import unittest
import xlsxwriter
from random import random

from pywindi.windrivers import SBIG_CCD
from pywindi.winclient import Winclient

file = open('ccd_base_config.txt', 'r')
image_path = file.readline()[:-1]
addresses = file.readline()[1:-1].replace(' ', '').split(',')


class TimeTest(unittest.TestCase):
    clinet = None
    device = None

    def test_time(self, host='localhost', port=7624):
        workbook = xlsxwriter.Workbook('time.xlsx')
        worksheet = workbook.add_worksheet()
        client = Winclient(host, int(port))
        device = client.get_device('SBIG CCD')
        device.configure(image_directory=image_path + str(addresses[0]) + '/')
        worksheet.write(0, 0, 'expected time')
        worksheet.write(0, 1, 'real time')
        for i in range(50):
            exposure_time = random() * 200 + 100
            tick = time.time()
            device.take_image(exposure_time)
            tick = time.time() - tick
            worksheet.write(i + 1, 0, exposure_time)
            worksheet.write(i + 1, 1, tick)
        workbook.close()


if __name__ == '__main__':
    unittest.main()
