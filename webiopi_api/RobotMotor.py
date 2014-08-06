__author__ = 'onebody'

# Imports
import webiopi

# Retrieve GPIO lib
GPIO = webiopi.GPIO

class RobotMotor():
    # Front motor GPIOs
    L1 = 22 # H-Bridge 1
    L2 = 27 # H-Bridge 2
    LS = 7 # H-Bridge 1,2EN

    # Back motor GPIOs
    R1 = 17 # H-Bridge 3
    R2 = 18 # H-Bridge 4
    RS = 9 # H-Bridge 3,4EN

    # -------------------------------------------------- #
    # Convenient PWM Function                            #
    # -------------------------------------------------- #

    # Set the speed of two motors
    def set_speed(self, speed):
        GPIO.pulseRatio(self.LS, speed)
        GPIO.pulseRatio(self.RS, speed)


    # -------------------------------------------------- #
    # Left Motor Functions                               #
    # -------------------------------------------------- #

    def left(self):
        GPIO.output(self.L1, GPIO.LOW)
        GPIO.output(self.L2, GPIO.HIGH)

    def right(self):
        GPIO.output(self.L1, GPIO.HIGH)
        GPIO.output(self.L2, GPIO.LOW)

    def stop(self):
        GPIO.output(self.L1, GPIO.LOW)
        GPIO.output(self.L2, GPIO.LOW)
        GPIO.output(self.R1, GPIO.LOW)
        GPIO.output(self.R2, GPIO.LOW)

    def forward(self):
        GPIO.output(self.R1, GPIO.HIGH)
        GPIO.output(self.R2, GPIO.LOW)

    def backward(self):
        GPIO.output(self.R1, GPIO.LOW)
        GPIO.output(self.R2, GPIO.HIGH)

    def init(self, L1, L2, LS, R1, R2, RS):
        # Setup GPIOs
        self.L1 = L1
        self.L2 = L2
        self.LS = LS
        self.R1 = R1
        self.R2 = R2
        self.RS = RS

        #    GPIO.setFunction(self.LS, GPIO.PWM)
        GPIO.setFunction(self.L1, GPIO.OUT)
        GPIO.setFunction(self.L2, GPIO.OUT)

        #    GPIO.setFunction(self.RS, GPIO.PWM)
        GPIO.setFunction(self.R1, GPIO.OUT)
        GPIO.setFunction(self.R2, GPIO.OUT)

