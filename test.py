import PyIndi
import windi
import time
import ctypes
import numpy as np
import cv2
from windi.agent import Agent

controller = windi.createNewController("v4l2 ccd")
agent = Agent(controller, controller.device)
for i in agent.getProperties():
    print(i, agent.getProperties()[i])
agent.setProperty('Image Adjustments', {'brightness': 100})

controller.initiateStreamMode(agent)

time.sleep(1)
blob = agent.getProperty("CCD1", True, 0)
while blob.blob == None:
    blob = agent.getProperty("CCD1", True, 0)
array = bytearray(ctypes.string_at(int(blob.blob), blob.size))
array = np.asarray(array, dtype = np.uint8)
array = np.reshape(array, (480, 640))
cv2.imshow("image", array)
cv2.waitKey()

controller.disconnectServer()
