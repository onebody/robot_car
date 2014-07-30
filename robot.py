__author__ = 'onebody'

import time
import RPi.GPIO as GPIO

class Robot_Car():
    distanceType_Before = 'Before'
    distanceType_After = 'After'

    delays = 2 #
    steps = 100 #


    def robot(self):
        try:
            rangingSensor = RangingSensor()

            stepMotor = StepMotor()

            while True:
                # Before Distance
                beforeDistance = rangingSensor.distance(self.distanceType_Before)
                afterDistance = rangingSensor.distance(self.distanceType_After)
                print "Before Distance : %.1f" % beforeDistance
                print "After Distance : %.1f" % afterDistance

                stepMotor.setup()
                stepMotor.initPin()
                if(beforeDistance > 15 ):
                    # Walk forward
                    print " Walk forward >>>>>"
                    #stepMotor.forward(self.delays, self.steps)
                elif(beforeDistance < 15 and afterDistance > 15 ):
                    # Back off
                    print "Back off <<<<<"
                    #stepMotor.backwards(self.delays, self.steps)
                elif(beforeDistance < 15 and afterDistance < 15 ):
                    if(beforeDistance > afterDistance):
                        # Forward left
                        print "Forward left <<<<<"
                    elif (beforeDistance <= afterDistance):
                        # Left rear back
                        print "Left rear back"

                time.sleep(1)

        except KeyboardInterrupt:
            # User pressed CTRL-C
            # Reset GPIO settings
            GPIO.cleanup()


class StepMotor():
    GPIO.setwarnings(False)

    coil_A_1_pin = 0
    coil_A_2_pin = 0

    coil_B_1_pin = 0
    coil_B_2_pin = 0


    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        self.coil_A_1_pin = 13 # GPIO 2
        self.coil_A_2_pin = 15 # GPIO 3

        self.coil_B_1_pin = 16 # GPIO 4
        self.coil_B_2_pin = 18 # GPIO 5


    def initPin(self):
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.output(self.coil_A_1_pin, False)

        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.output(self.coil_A_2_pin, False)

        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.output(self.coil_B_1_pin, False)

        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)
        GPIO.output(self.coil_B_2_pin, False)


    def backwards(self, delays, steps):
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


    def forward(self, delays, steps):
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

        GPIO.cleanup()
        return distance

    def distance(self, type):
        # Define GPIO to use on Pi
        GPIO_TRIGGER = 0
        GPIO_ECHO = 0

        if(type == 'Before'):
            GPIO_TRIGGER = 11 # GPIO 0
            GPIO_ECHO = 12 # GPIO 1
        elif(type == 'After'):
            GPIO_TRIGGER = 5 # SCL
            GPIO_ECHO = 8 # TXD
        else:
            return 0

        if(GPIO_TRIGGER == 0 or GPIO_ECHO == 0):
            return 0
        else:
            return self.measure(GPIO_TRIGGER, GPIO_ECHO)


robot = Robot_Car()

robot.robot()
