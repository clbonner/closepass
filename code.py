# entry point for running the close pass data logger

from closepass import *
from closepass_gps import *

waitForGPSReady()

while True:
    distance = getDistance()
    if (isClosePass(distance)):
        logClosePass(distance)