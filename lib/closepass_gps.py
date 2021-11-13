import board, busio, adafruit_gps

uart = busio.UART(board.GP4, board.GP4, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart)

def waitForGPSReady():
    while not gps.has_fix:
        pass
    
    return True

def getGPSLocation():
    location = gps.readline()
    if not location:
        return "Signal lost"