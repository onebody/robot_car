__author__ = 'onebody'

import time
import RPi.GPIO as GPIO

class Robot_Car():
    distanceType_Before = 'Before'
    distanceType_After = 'After'

    delays = 0.5 #
    steps = 100 #


    def robot(self):
        try:
            rangingSensor = RangingSensor()

            motor = Motor()

            while True:
                # Before Distance
                beforeDistance = rangingSensor.distance(self.distanceType_Before)
                afterDistance = rangingSensor.distance(self.distanceType_After)
                print("Before Distance : %.1f" % beforeDistance)
                print("After Distance : %.1f" % afterDistance)

                if(beforeDistance > 15 ):
                    # Walk forward
                    print(" Walk forward >>>>>")
                    motor.forward(self.delays)
                elif(beforeDistance < 15 and afterDistance > 15 ):
                    # Back off
                    print("Back off <<<<<")
                    motor.backwards(self.delays)
                elif(beforeDistance < 15 and afterDistance < 15 ):
                    if(beforeDistance > afterDistance):
                        # Forward left
                        print("Forward left <<<<<")
                        motor.forward_Left(self.delays)
                    elif (beforeDistance <= afterDistance):
                        # Left rear back
                        print("Left rear back")
                        motor.back_Left(self.delays)

                time.sleep(2)

        except KeyboardInterrupt:
            # User pressed CTRL-C
            # Reset GPIO settings
            GPIO.cleanup()


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
        self.setup()
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


class StepMotor():
    GPIO.setwarnings(False)

    coil_A_1_pin = 0
    coil_A_2_pin = 0

    coil_B_1_pin = 0
    coil_B_2_pin = 0


    def setup(self):
        GPIO.setmode(GPIO.BCM)
        self.coil_A_1_pin = 8 # CE0
        self.coil_A_2_pin = 11 # SCLK

        self.coil_B_1_pin = 25 # GPIO 6
        self.coil_B_2_pin = 7 #  CE1


    def initPin(self):
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.output(self.coil_A_1_pin, False)

        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.output(self.coil_A_2_pin, False)

        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.output(self.coil_B_1_pin, False)

        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)
        GPIO.output(self.coil_B_2_pin, False)


    def right(self, delays, steps):
        delay = delays / 1000.0

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


    def left(self, delays, steps):
        delay = delays / 1000.0

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


class RangingSensor():
    GPIO.setwarnings(False)

    def measure(self, GPIO_TRIGGER=0, GPIO_ECHO=0):
        GPIO.setmode(GPIO.BCM)
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

        GPIO.cleanup()
        return distance

    def distance(self, type):
        # Define GPIO to use on Pi
        GPIO_TRIGGER = 0
        GPIO_ECHO = 0

        if(type == 'Before'):
            GPIO_TRIGGER = 23 # GPIO 4
            GPIO_ECHO = 24 # GPIO 5
        elif(type == 'After'):
            GPIO_TRIGGER = 1 # SCL
            GPIO_ECHO = 4 # GPIO7
        else:
            return 0

        if(GPIO_TRIGGER == 0 or GPIO_ECHO == 0):
            return 0
        else:
            return self.measure(GPIO_TRIGGER, GPIO_ECHO)


robot = Robot_Car()

robot.robot()
