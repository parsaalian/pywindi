import PyIndi
import windi
import time
import ctypes
import numpy as np
import cv2

controller = windi.createNewController("v4l2 ccd")
controller.printProperties()
controller.initiateStreamMode()

tick = time.time()
while time.time() - tick <= 15:
    blob = controller.getProperty("CCD1", 'blob', 0)
    while blob.blob == None:
        blob = controller.getProperty("CCD1", 'blob', 0)
    array = bytearray(ctypes.string_at(int(blob.blob), blob.size))
    array = np.asarray(array, dtype = np.uint8)
    array = np.reshape(array, (480, 640))
    cv2.imshow("Cameras", array)
    cv2.waitKey(1)

controller.disconnectServer()
