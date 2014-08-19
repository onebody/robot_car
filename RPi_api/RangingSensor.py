#!/usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

class RangingSensor():
    def measure(self, GPIO_TRIGGER=0, GPIO_ECHO=0):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)

        GPIO.output(GPIO_TRIGGER, False)

        start = 0
        stop = 0

        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()

        while GPIO.input(GPIO_ECHO) == 0:
            start = time.time()

        while GPIO.input(GPIO_ECHO) == 1:
            stop = time.time()

        elapsed = stop - start
        distance = (elapsed * 34300) / 2

        GPIO.output(GPIO_TRIGGER, False)
        return distance


    def distance(self, type):
        # Define GPIO to use on Pi
        GPIO_TRIGGER = 0
        GPIO_ECHO = 0

        if(type == 'Before'):
            GPIO_TRIGGER = 16 # GPIO 4
            GPIO_ECHO = 18 # GPIO 5
        elif(type == 'After'):
            GPIO_TRIGGER = 5 # SCL
            GPIO_ECHO = 7 # GPIO7
        else:
            return 0

        if(GPIO_TRIGGER == 0 or GPIO_ECHO == 0):
            return 0
        else:
            return self.measure(GPIO_TRIGGER, GPIO_ECHO)


#
#rangingSensor = RangingSensor()
#beforeDistance = rangingSensor.measure(16, 18)
#print("Before Distance : %.1f" % beforeDistance)
#afterDistance = rangingSensor.measure(5, 7)
#print("After Distance : %.1f" % afterDistance)
