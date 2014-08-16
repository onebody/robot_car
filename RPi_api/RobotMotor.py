#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

class RobotMotor():
    # Front motor GPIOs
    L1 = 15 # H-Bridge 1
    L2 = 13 # H-Bridge 2
    LS = 7 # H-Bridge 1,2EN

    # Back motor GPIOs
    R1 = 11 # H-Bridge 3
    R2 = 12 # H-Bridge 4
    RS = 9 # H-Bridge 3,4EN

    # -------------------------------------------------- #
    # Convenient PWM Function                            #
    # -------------------------------------------------- #

    # Set the speed of two motors
    def set_speed(self, speed):
    #        GPIO.pulseRatio(self.LS, speed)
    #        GPIO.pulseRatio(self.RS, speed)
        print()


    # -------------------------------------------------- #
    # Left Motor Functions                               #
    # -------------------------------------------------- #

    def left(self):
        GPIO.output(self.L1, False)
        GPIO.output(self.L2, True)

    def right(self):
        GPIO.output(self.L1, True)
        GPIO.output(self.L2, False)

    def stop(self):
        GPIO.output(self.L1, False)
        GPIO.output(self.L2, False)
        GPIO.output(self.R1, False)
        GPIO.output(self.R2, False)

    def forward(self):
        GPIO.output(self.R1, True)
        GPIO.output(self.R2, False)

    def backward(self):
        GPIO.output(self.R1, False)
        GPIO.output(self.R2, True)

    def init(self, L1, L2, LS, R1, R2, RS):
        # Setup GPIOs
        self.L1 = L1
        self.L2 = L2
        self.LS = LS
        self.R1 = R1
        self.R2 = R2
        self.RS = RS
#        print("L1=%d,L2=%d,LS=%d,R1=%d,R2=%d,RS=%d " % (L1 , L2 , LS , R1 , R2 , RS))

        GPIO.setmode(GPIO.BOARD)
        #    GPIO.setFunction(self.LS, GPIO.PWM)
        GPIO.setup(self.L1, GPIO.OUT)
        GPIO.setup(self.L2, GPIO.OUT)

        #    GPIO.setFunction(self.RS, GPIO.PWM)
        GPIO.setup(self.R1, GPIO.OUT)
        GPIO.setup(self.R2, GPIO.OUT)


#motor = RobotMotor()
#motor.init(15, 13, 7, 11, 12, 9)
#
#print(" Walk forward >>>>>")
#motor.forward()