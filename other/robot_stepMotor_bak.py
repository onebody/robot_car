#-----------------------------------
# Name: bujindianji
# Created: 03/16/2014
#-----------------------------------
#!/usr/bin/env python

# Import required libraries
import time
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
coil_A_1_pin = 0
coil_A_2_pin = 0

coil_B_1_pin = 0
coil_B_2_pin = 0

#print  " GPIO  BCM"
#GPIO.setmode(GPIO.BCM)
#coil_A_1_pin = 17
#coil_A_2_pin = 18
#
#coil_B_1_pin = 27
#coil_B_2_pin = 22


print  " GPIO  BOARD"
GPIO.setmode(GPIO.BOARD)
coil_A_1_pin = 11
coil_A_2_pin = 12

coil_B_1_pin = 13
coil_B_2_pin = 15

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.output(coil_A_1_pin, False)

GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.output(coil_A_2_pin, False)

GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.output(coil_B_1_pin, False)

GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.output(coil_B_2_pin, False)


def backwards(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)

        setStep(0, 0, 0, 1)
        time.sleep(delay)

        setStep(0, 0, 1, 1)
        time.sleep(delay)

        setStep(0, 0, 1, 0)
        time.sleep(delay)

        setStep(0, 1, 1, 0)
        time.sleep(delay)

        setStep(0, 1, 0, 0)
        time.sleep(delay)

        setStep(1, 1, 0, 0)
        time.sleep(delay)

        setStep(1, 0, 0, 0)
        time.sleep(delay)


def forward(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 0, 0)
        time.sleep(delay)

        setStep(1, 1, 0, 0)
        time.sleep(delay)

        setStep(0, 0, 0, 0)
        time.sleep(delay)

        setStep(0, 1, 1, 0)
        time.sleep(delay)

        setStep(0, 0, 1, 0)
        time.sleep(delay)

        setStep(0, 0, 1, 1)
        time.sleep(delay)

        setStep(0, 0, 0, 1)
        time.sleep(delay)

        setStep(1, 0, 0, 1)
        time.sleep(delay)


def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)

    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)


while True:
    delay = raw_input("Delay between steps (milliseconds)?")
    steps = raw_input("How many steps forward? ")
    forward(int(delay) / 1000.0, int(steps))

    steps = raw_input("How many steps backwards? ")
    backwards(int(delay) / 1000.0, int(steps))