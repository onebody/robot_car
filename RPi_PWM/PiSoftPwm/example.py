# The original is aboudou ,the Source code is here : https://goddess-gate.com/dc2/index.php/pages/raspiledmeter.en
# The modifier is ukonline2000
#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import signal

from PiSoftPwm import *

# Called on process interruption. Set all pins to "Input" default mode.
def endProcess(signalnum = None, handler = None):
    first.stop()
    second.stop()
    third.stop()
    fourth.stop()
    fifth.stop()
    sixth.stop()
    seventh.stop()
    eighth.stop()

    GPIO.cleanup()
    exit(0)

# Prepare handlers for process exit
signal.signal(signal.SIGTERM, endProcess)
signal.signal(signal.SIGINT, endProcess)

# Initialize PWM outputs
#PiSoftPwm(baseTime, nbSlices, gpioPin, gpioScheme)
#Init the PiSoftPwm instance. Expected parameters are :
#baseTime : the base time in seconds for the PWM pattern. You may choose a small value (i.e 0.01 s)
#nbSlices : the number of divisions of the PWM pattern. A single pulse will have a min duration of baseTime * (1 / nbSlices)
#gpioPin : the pin number which will act as PWM ouput
#gpioScheme : the GPIO naming scheme (see RPi.GPIO documentation)

first   = PiSoftPwm(0.01, 100, 17, GPIO.BCM)
second  = PiSoftPwm(0.01, 100, 18, GPIO.BCM)
third   = PiSoftPwm(0.01, 100, 27, GPIO.BCM)  #for raspberry pi rev 2.0
#third   = PiSoftPwm(0.01, 100, 21, GPIO.BCM)  #for raspberry pi rev 1.0
fourth  = PiSoftPwm(0.01, 100, 22, GPIO.BCM)
fifth   = PiSoftPwm(0.01, 100, 23, GPIO.BCM)
sixth   = PiSoftPwm(0.01, 100, 24, GPIO.BCM)
seventh = PiSoftPwm(0.01, 100, 25, GPIO.BCM)
eighth  = PiSoftPwm(0.01, 100, 4, GPIO.BCM)

# Initialize directions 
#  "up" = we will allocate more and more time to HIGH output (aka the LED will be brighter)
#  "down" = we will allocate less and less time to HIGH output (aka the LED will be dimmer)
directions = ["up", "up", "up", "up", "up", "up", "up", "up"]

# Initialize the starting number of slices of HIGH output
#slices = [0, 14, 28, 42, 56, 70, 84, 100]
slices = [0, 0, 0, 0, 0, 0, 0, 0]


#Start PWM output. Expected parameter is : start(nbSlicesOn):
#nbSlicesOn : number of divisions (on a total of nbSlices - see init() doc) to set HIGH output on the GPIO pin
#Exemple : with a total of 100 slices, a baseTime of 1 second, and an nbSlicesOn set to 25, the PWM pattern will
#          have a duty cycle of 25%. With a duration of 1 second, will stay HIGH for 1*(25/100) seconds on HIGH 
#          output, and1*(75/100) seconds on LOW output.
first.start(slices[0])
second.start(slices[1])
third.start(slices[2])
fourth.start(slices[3])
fifth.start(slices[4])
sixth.start(slices[5])
seventh.start(slices[6])
eighth.start(slices[7])

while True:

  # Change number of slices of HIGH output
  first.changeNbSlicesOn(slices[0])
  second.changeNbSlicesOn(slices[1])
  third.changeNbSlicesOn(slices[2])
  fourth.changeNbSlicesOn(slices[3])
  fifth.changeNbSlicesOn(slices[4])
  sixth.changeNbSlicesOn(slices[5])
  seventh.changeNbSlicesOn(slices[6])
  eighth.changeNbSlicesOn(slices[7])
  time.sleep(0.01)

  i = 0
  while i < len(slices): 
    if slices[i] == 100:
      directions[i]="down"
    if slices[i] == 0:
      directions[i]="up"
    i += 1

  i = 0
  while i < len(directions):
    if directions[i] == "up":
      slices[i] += 1
    if directions[i] == "down":
      slices[i] -= 1
    i += 1

