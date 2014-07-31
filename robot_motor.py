__author__ = 'onebody'

import RPi.GPIO as GPIO
import time

class Motor():
    GPIO.setwarnings(False)

    IN1 = 15 #GPIO 3  IN1
    IN2 = 13 #GPIO 2  IN2
    IN3 = 11 #GPIO 0  IN3
    IN4 = 12 #GPIO 1  IN4

    def setup(self):
        GPIO.setmode(GPIO.BOARD)

    def initPin12(self):
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN1, GPIO.OUT)

    def initPin34(self):
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)

    def turn_Left(self, delay):
        self.setup()
        self.initPin12()
        GPIO.output(self.IN2, True)
        GPIO.output(self.IN1, False)
        time.sleep(delay)
        GPIO.cleanup()

    def turn_Right(self, delay):
        self.setup()
        self.initPin12()
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN1, True)
        time.sleep(delay)
        GPIO.cleanup()

    def forward(self, delay):
        self.setup()
        self.initPin34()
        GPIO.output(self.IN4, False)
        GPIO.output(self.IN3, True)
        time.sleep(delay)
        GPIO.cleanup()

    def backwards(self, delay):
        self.initPin34()
        GPIO.output(self.IN4, True)
        GPIO.output(self.IN3, False)
        time.sleep(delay)
        GPIO.cleanup()

    def forward_Left(self, delay):
        self.setup()
        self.initPin12()
        self.initPin34()
        GPIO.output(self.IN2, True)
        GPIO.output(self.IN1, False)

        GPIO.output(self.IN4, False)
        GPIO.output(self.IN3, True)
        time.sleep(delay)
        GPIO.cleanup()

    def forward_Right(self, delay):
        self.setup()
        self.initPin12()
        self.initPin34()
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN1, True)

        GPIO.output(self.IN4, False)
        GPIO.output(self.IN3, True)
        time.sleep(delay)
        GPIO.cleanup()

    def back_Left(self, delay):
        self.setup()
        self.initPin12()
        self.initPin34()
        GPIO.output(self.IN2, True)
        GPIO.output(self.IN1, False)

        GPIO.output(self.IN4, True)
        GPIO.output(self.IN3, False)
        time.sleep(delay)
        GPIO.cleanup()

    def back_Right(self, delay):
        self.setup()
        self.initPin12()
        self.initPin34()
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN1, True)

        GPIO.output(self.IN4, True)
        GPIO.output(self.IN3, False)
        time.sleep(delay)
        GPIO.cleanup()


delay = 2

motor = Motor()
print "turn left >>>>\n"
motor.turn_Left(delay)

time.sleep(delay)

print "turn right >>>>\n"
motor.turn_Right(delay)

print "forward >>>>\n"
motor.forward(delay)

time.sleep(delay)

print "back wards >>>>\n"
motor.backwards(delay)

time.sleep(delay)

print "forward left >>>>\n"
motor.forward_Left(delay)

time.sleep(delay)

print "forward right >>>>\n"
motor.forward_Right(delay)

time.sleep(delay)
print "back left >>>>\n"
motor.back_Left(delay)

time.sleep(delay)

print "back right >>>>\n"
motor.back_Right(delay)
