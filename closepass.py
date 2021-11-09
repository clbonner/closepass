import time
import board
import adafruit_hcsr04
import digitalio
import pwmio

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP0, echo_pin=board.GP1)
buzzer = pwmio.PWMOut(board.GP2, duty_cycle = 0, frequency = 800)
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

def checkDistance():
    if (sonar.distance > 30 and sonar.distance < 150):
        closePass(sonar.distance)
    time.sleep(0.2)
    return

def closePass(distance):
    closestDistance = distance
    led.value = True
    buzzer.duty_cycle = 2000
    
    while (sonar.distance > 30 and sonar.distance < 150):
        if sonar.distance < closestDistance:
            closestDistance = sonar.distance
        time.sleep(0.2)

    led.value = False
    buzzer.duty_cycle = 0
    logClosePass(closestDistance)


# store close pass distance on local datastore
# if storage full then write over log
def logClosePass(distance):
    print("Closest Distance:", distance)
    

while True:
    checkDistance()