# gps functions for closepass

def waitForGPSReady():
    while not gps.has_fix:
        pass
    
    return True

def getGPSLocation():
    location = gps.readline()
    if not location:
        return "Signal lost"