# entry point for running the close pass data logger

from closepass import *

waitForGPSReady()

while True:
    distance = getDistance()
    if (isClosePass(distance)):
        logClosePass(distance)