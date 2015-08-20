#!/usr/bin/python
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

class RobotMotor():
    # Front motor GPIOs
    OUT1 = 15 # H-Bridge 1
    OUT2 = 13 # H-Bridge 2
    EN1 = 7 # H-Bridge 1,2EN

    # Back motor GPIOs
    OUT3 = 11 # H-Bridge 3
    OUT4 = 12 # H-Bridge 4
    EN2 = 9 # H-Bridge 3,4EN

    # -------------------------------------------------- #
    # Convenient PWM Function                            #
    # -------------------------------------------------- #

    # Set the speed of two motoEN2
    def set_speed(self, speed):
    #        GPIO.puEN1eRatio(self.EN1, speed)
    #        GPIO.puEN1eRatio(self.EN2, speed)
        print()


    # -------------------------------------------------- #
    # Left Motor Functions                               #
    # -------------------------------------------------- #

    def left(self):
        GPIO.output(self.OUT1, False)
        GPIO.output(self.OUT2, True)

    def right(self):
        GPIO.output(self.OUT1, True)
        GPIO.output(self.OUT2, False)

    def stop(self):
        GPIO.output(self.OUT1, False)
        GPIO.output(self.OUT2, False)
        GPIO.output(self.OUT3, False)
        GPIO.output(self.OUT4, False)

    def forward(self):
        GPIO.output(self.OUT3, True)
        GPIO.output(self.OUT4, False)

    def backward(self):
        GPIO.output(self.OUT3, False)
        GPIO.output(self.OUT4, True)

    def init(self, OUT1, OUT2, EN1, OUT3, OUT4, EN2):
        # Setup GPIOs
        self.OUT1 = OUT1
        self.OUT2 = OUT2
        self.EN1 = EN1
        self.OUT3 = OUT3
        self.OUT4 = OUT4
        self.EN2 = EN2
        #        print("OUT1=%d,OUT2=%d,EN1=%d,OUT3=%d,OUT4=%d,EN2=%d " % (OUT1 , OUT2 , EN1 , OUT3 , OUT4 , EN2))

        GPIO.setmode(GPIO.BOARD)
        #    GPIO.setFunction(self.EN1, GPIO.PWM)
        GPIO.setup(self.OUT1, GPIO.OUT)
        GPIO.setup(self.OUT2, GPIO.OUT)

        #    GPIO.setFunction(self.EN2, GPIO.PWM)
        GPIO.setup(self.OUT3, GPIO.OUT)
        GPIO.setup(self.OUT4, GPIO.OUT)


        #motor = RobotMotor()
        #motor.init( 11, 12, 9, 15, 13, 7)
        #
        #print(" Walk forward >>>>>")
        #motor.forward()