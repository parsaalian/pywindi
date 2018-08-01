import PyIndi
from pywindi.winclient import Winclient
from math import sin, cos, radians, atan, pow
import time
import ctypes
import numpy as np
import cv2

client = Winclient('192.168.150.72')
webcam = client.get_device('V4L2 CCD', DEVICE_PORT=['/dev/video1'])
webcam.set_property("Image Adjustments", [20, 150, None, None, None, None, None, None, None, None, None, None])

def seeing(device, buffer_time=60, D=0.003, S=0.05, lmbd=0.00000055):
    device.initiate_stream_mode()
    tick = time.time()
    centers = []
    while time.time() - tick <= buffer_time:
        C = [0, 0]
        blob = client.blob_queue['V4L2 CCD'].pop()[1]
        shape = (480, 640)
        array = np.ndarray(buffer = memoryview((ctypes.c_uint8 * blob.size).from_address(int(blob.blob))), shape = shape, dtype = np.uint8)
        circles = cv2.HoughCircles(array, cv2.HOUGH_GRADIENT, 5, 15, param1 = 36, param2 = 36, minRadius = 1, maxRadius = 10)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(array, (x, y), r, (0, 255, 0), 2)
                cv2.rectangle(array, (x - 1, y - 1), (x + 1, y + 1), (0, 128, 255), -1)
            if len(circles) == 2:
                C[0] = (circles[0][0] - circles[1][0])
                C[1] = (circles[0][1] - circles[1][1])
                if C[0] < 0:
                    C[0] = -1 * C[0]
                    C[1] = -1 * C[1]
                centers.append(C)
        cv2.imshow("Cameras", array)
        cv2.waitKey(1)
    centers = np.array(centers)
    meanX = np.mean([item[0] for item in centers])
    meanY = np.mean([item[1] for item in centers])
    theta = atan(meanY / meanX)
    rotated = np.array([[(center[0] * cos(theta) + center[1] * sin(theta)) for center in centers], [(center[0] * sin(theta) - center[1] * cos(theta)) for center in centers]])
    varX = np.var(rotated[0])
    varY = np.var(rotated[1])
    b = S / D
    kl = 0.364 * (1 - 0.532 * pow(b, -1 / 3) - 0.024 * pow(b, -7 / 3))
    kt = 0.364 * (1 - 0.798 * pow(b, -1 / 3) - 0.018 * pow(b, -7 / 3))
    epsilon1 = 0.976 * pow((D / lmbd), 0.2) * pow(abs((varX - varY) / kl) , 0.6)
    epsilon2 = 0.976 * pow((D / lmbd), 0.2) * pow(abs((varX - varY) / kt) , 0.6)
    return ((epsilon1 + epsilon2) / 2)

print (seeing(webcam, 35))

client.disconnectServer()
