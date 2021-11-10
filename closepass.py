import time
import board
import adafruit_hcsr04
import digitalio
import pwmio

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP0, echo_pin=board.GP1)
buzzer = pwmio.PWMOut(board.GP2, duty_cycle = 0, frequency = 800)
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

def tooClose():
    try:
        if (sonar.distance > 30 and sonar.distance < 150):
            return sonar.distance;
    except RuntimeError:
        pass # just try again
    
    return False

def closePass(distance):
    closestDistance = distance
    led.value = True
    buzzer.duty_cycle = 2000
    
    while (distance = tooClose()):
        if distance < closestDistance:
            closestDistance = distance

    led.value = False
    buzzer.duty_cycle = 0
    logClosePass(closestDistance)


# store close pass distance on local datastore
# if storage full then write over log
def logClosePass(distance):
    print("Closest Distance:", distance)
