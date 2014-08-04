__author__ = 'onebody'

import webiopi
import time

# Retrieve GPIO lib
GPIO = webiopi.GPIO


class RangingSensor():
    def measure(self, GPIO_TRIGGER=0, GPIO_ECHO=0):
        GPIO.setFunction(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setFunction(GPIO_ECHO, GPIO.IN)

        GPIO.output(GPIO_TRIGGER, GPIO.LOW)

        start = 0
        stop = 0

        GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
        start = time.time()

        while GPIO.input(GPIO_ECHO) == 0:
            start = time.time()

        while GPIO.input(GPIO_ECHO) == 1:
            stop = time.time()

        elapsed = stop - start
        distance = (elapsed * 34300) / 2

        GPIO.output(GPIO_TRIGGER, GPIO.LOW)
        return distance

    def distance(self, type):
        # Define GPIO to use on Pi
        GPIO_TRIGGER = 0
        GPIO_ECHO = 0

        if(type == 'Before'):
            GPIO_TRIGGER = 23 # GPIO 4
            GPIO_ECHO = 24 # GPIO 5
        elif(type == 'After'):
            GPIO_TRIGGER = 3 # SCL
            GPIO_ECHO = 4 # GPIO 7
        else:
            return 0

        if(GPIO_TRIGGER == 0 or GPIO_ECHO == 0):
            return 0
        else:
            return self.measure(GPIO_TRIGGER, GPIO_ECHO)