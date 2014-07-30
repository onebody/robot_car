#-----------------------------------
# Name: bujindianji
# Created: 03/16/2014
#-----------------------------------
#!/usr/bin/env python

# Import required libraries
import time
import RPi.GPIO as GPIO


class StepMotor():
    GPIO.setwarnings(False)

    coil_A_1_pin = 0
    coil_A_2_pin = 0

    coil_B_1_pin = 0
    coil_B_2_pin = 0


    def setup(self, type):
    #    if (type == "BCM"):

    #    print  type
        if (type == 'BCM'):
            print  " GPIO  BCM"
            GPIO.setmode(GPIO.BCM)
            self.coil_A_1_pin = 17
            self.coil_A_2_pin = 18

            self.coil_B_1_pin = 27
            self.coil_B_2_pin = 22
        else:
            print  " GPIO  BOARD"
            GPIO.setmode(GPIO.BOARD)
            self.coil_A_1_pin = 11
            self.coil_A_2_pin = 12

            self.coil_B_1_pin = 13
            self.coil_B_2_pin = 15


    def initPin(self):
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.output(self.coil_A_1_pin, False)

        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.output(self.coil_A_2_pin, False)

        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.output(self.coil_B_1_pin, False)

        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)
        GPIO.output(self.coil_B_2_pin, False)


    def backwards(self, delay, steps):
        for i in range(0, steps):
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)

            self.setStep(0, 0, 0, 1)
            time.sleep(delay)

            self.setStep(0, 0, 1, 1)
            time.sleep(delay)

            self.setStep(0, 0, 1, 0)
            time.sleep(delay)

            self.setStep(0, 1, 1, 0)
            time.sleep(delay)

            self.setStep(0, 1, 0, 0)
            time.sleep(delay)

            self.setStep(1, 1, 0, 0)
            time.sleep(delay)

            self.setStep(1, 0, 0, 0)
            time.sleep(delay)


    def forward(self, delay, steps):
        for i in range(0, steps):
            self.setStep(1, 0, 0, 0)
            time.sleep(delay)

            self.setStep(1, 1, 0, 0)
            time.sleep(delay)

            self.setStep(0, 0, 0, 0)
            time.sleep(delay)

            self.setStep(0, 1, 1, 0)
            time.sleep(delay)

            self.setStep(0, 0, 1, 0)
            time.sleep(delay)

            self.setStep(0, 0, 1, 1)
            time.sleep(delay)

            self.setStep(0, 0, 0, 1)
            time.sleep(delay)

            self.setStep(1, 0, 0, 1)
            time.sleep(delay)


    def setStep(self, w1, w2, w3, w4):
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)

        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    def start(self):
        self.setup('BCM')
        self.initPin()

        while True:
            delay = raw_input("Delay between steps (milliseconds)?")
            steps = raw_input("How many steps forward? ")
            self.forward(int(delay) / 1000.0, int(steps))

            steps = raw_input("How many steps backwards? ")
            self.backwards(int(delay) / 1000.0, int(steps))

stepMotor = StepMotor()

stepMotor.start()