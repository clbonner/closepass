# entry point for running the close pass data logger

from closepass import *

while True:
    distance = getDistance()
    if(isClosePass(distance)):
        logClosePass(distance)