import time, board, adafruit_hcsr04, digitalio, pwmio, busio, adafruit_gps, sdcardio, storage

class closepass:
    def __init__(self):
        # upper and lower distances for sensor
        self.UPPER = 150
        self.LOWER = 30

        # initialize devices
        self.sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP16, echo_pin=board.GP17)
        self.led = digitalio.DigitalInOut(board.GP25)
        self.led.direction = digitalio.Direction.OUTPUT
        self.uart = busio.UART(board.GP4, board.GP5, baudrate=9600, timeout=10)
        self.gps = adafruit_gps.GPS(self.uart)
        self.spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
        self.cs = board.GP13

        # mount sdcard
        self.sdcard = sdcardio.SDCard(self.spi, self.cs)
        self.vfs = storage.VfsFat(self.sdcard)
        storage.mount(self.vfs, "/sd")
    
    # returns sensor distance
    def getDistance(self):
        try:
            time.sleep(0.5)
            return self.sonar.distance
        except RuntimeError:
            pass # just try again

    # checks if a close pass has occurred
    def isClosePass(self, distance):
        if (distance > self.LOWER and distance < self.UPPER):
            return True
        else:
            return False
        
    # get closest distance of vehicle and GPS location, log on SD card
    def logClosePass(self, distance):
        closestDistance = distance
        furthestDistance = distance
        self.led.value = True
        
        # open log file
        log = open("/sd/closepass_log.txt", "a")
        
        # get furthest and closest distance as the car passes
        while self.isClosePass(distance):
            distance = self.getDistance()
            if self.isClosePass(distance) and distance < closestDistance:
                closestDistance = distance
            if self.isClosePass(distance) and distance > furthestDistance:
                furthestDistance = distance
        
        self.led.value = False

        print(f"Closest Distance: {closestDistance}")
        print(f"Furthest Distance: {furthestDistance}")
        print(self.getGPSLocation())
        log.write(f"Closest Distance: {closestDistance}\n")
        log.write(f"Furthest Distance: {furthestDistance}\n")
        
        log.close()

    # wait for GPD module to get satelites
    def waitForGPSReady(self):
        # Turn on the basic GGA and RMC info
        self.gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Set update rate to once a second (1hz)
        self.gps.send_command(b'PMTK220,1000')

        print("Waiting for GPS...")
        while not self.gps.has_fix:
            continue
        
        print("GPS Ready")
        return

    def getGPSLocation(self):
        self.gps.update()
        location = self.gps.readline()
        if not location:
            return "Signal lost"
        return location
        
    # main loop for logger
    def run(self):
        self.waitForGPSReady()
        print("Ready")
        
        while True:
            distance = self.getDistance()
            if (self.isClosePass(distance)):
                self.logClosePass(distance)

