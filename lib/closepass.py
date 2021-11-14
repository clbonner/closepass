import time, board, adafruit_hcsr04, digitalio, pwmio, busio, adafruit_gps
import closepass_gps

# upper and lower distances for sensor
UPPER = 150
LOWER = 30

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP16, echo_pin=board.GP17)
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
uart = busio.UART(board.GP4, board.GP4, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart)

# returns sensor distance
def getDistance():
    try:
        time.sleep(0.5)
        return sonar.distance
    except RuntimeError:
        pass # just try again

# checks if a close pass has occurred
def isClosePass(distance):
    if (distance > LOWER and distance < UPPER):
        return True
    else:
        return False
    
# get closest distance of vehicle and GPS location, log on SD card
def logClosePass(distance):
    closestDistance = distance
    furthestDistance = distance
    led.value = True
    
    # get furthest and closest distance as the car passes
    while isClosePass(distance):
        distance = getDistance()
        if isClosePass(distance) and distance < closestDistance:
            closestDistance = distance
        if isClosePass(distance) and distance > furthestDistance:
            furthestDistance = distance

    # GPS location to implement
    
    led.value = False

    print("Closest Distance:", closestDistance)
    print("Furthest Distance: ", furthestDistance)
    
    # SD card to implement
    buzzer.duty_cycle = 0

