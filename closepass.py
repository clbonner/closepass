import time
import board
import adafruit_hcsr04
import digitalio
import pwmio

# upper and lower distances for sensor
UPPER = 150
LOWER = 30

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP0, echo_pin=board.GP1)
buzzer = pwmio.PWMOut(board.GP2, duty_cycle = 0, frequency = 800)
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

# returns sensor distance
def getDistance():
    try:
        time.sleep(0.5)
        return sonar.distance
    except RuntimeError:
        pass # just try again

# checks if a close pass has occurred
def isClosePass(distance):
    True if distance > LOWER and distance < UPPER else False
    
# get closest distance of vehicle and GPS location, log on SD card
def logClosePass(distance):
    closestDistance = distance
    led.value = True
    buzzer.duty_cycle = 2000
    
    while isClosePass(distance):
        distance = getDistance()
        if isClosePass(distance) and distance < closestDistance:
            closestDistance = distance

    # GPS location to implement
    
    led.value = False
    buzzer.duty_cycle = 0

    print("Closest Distance:", closestDistance)
    
    # SD card to implement
