#!/usr/bin/env python
#-*- coding: utf-8 -*-
#coding=utf-8

import RPi.GPIO as gpio
import time


gpio.setwarnings(False)

def distance(measure='cm', GPIO_TRIGGER=0, GPIO_ECHO=0):
# Define GPIO to use on Pi
#    GPIO_TRIGGER = 12
#    GPIO_ECHO = 16

    gpio.setmode(gpio.BOARD)
    gpio.setup(GPIO_TRIGGER, gpio.OUT)
    gpio.setup(GPIO_ECHO, gpio.IN)

    gpio.output(GPIO_TRIGGER, False)

    start = 0
    stop = 0

    gpio.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    gpio.output(GPIO_TRIGGER, False)
    start = time.time()

    while gpio.input(GPIO_ECHO) == 0:
        start = time.time()

    while gpio.input(GPIO_ECHO) == 1:
        stop = time.time()

    elapsed = stop - start
    #    distance = (elapsed * 34300) / 2


    if measure == 'cm':
        distance = elapsed / 0.000058
    elif measure == 'in':
        distance = elapsed / 0.000148
    else:
        print ('improper choice of measurement : in or cm')
        distance = None

    gpio.cleanup()
    return distance

print ('No1.distance: ' + str(distance('cm', 11, 12)) + ' cm')

print ('No2.distance: ' + str(distance('cm', 5, 8)) + ' cm')

