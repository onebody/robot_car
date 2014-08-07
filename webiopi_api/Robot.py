# This version uses new-style automatic setup/destroy/mapping
# Need to change /etc/webiopi

# Imports
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


class StepMotor():
    ports = [8, 11, 25, 7]

    def turnWebcam(self, steps_str, clockwise_str, delay):
        steps = int(steps_str)

        clockwise = int(clockwise_str)

        arr = [0, 1, 2, 3]

        if clockwise != 1:
            arr = [3, 2, 1, 0]

        ports = self.ports

        for p in ports:
            GPIO.setFunction(p, GPIO.OUT)

        for x in range(0, steps):
            for j in arr:
                time.sleep(float(delay))

                for i in range(0, 4):
                    if i == j:
                        GPIO.output(ports[i], GPIO.LOW)

                    else:
                        GPIO.output(ports[i], GPIO.HIGH)


    def setup(self, in1, in2, in3, in4):
        self.ports = [int(in1), int(in2), int(in3), int(in4)]

    def destroy(self):
        for p in self.ports:
            GPIO.setFunction(p, GPIO.IN)


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


class Robot_Car():
    distanceType_Before = 'Before'
    distanceType_After = 'After'

    isAuto = True

    delays = 0.5 #
    steps = 100 #

    def stop(self):
        self.isAuto = False

    def start(self):
        try:
            rangingSensor = RangingSensor()

            motor = RobotMotor()

            while True:
                if(self.isAuto == True):
                    # Before Distance
                    beforeDistance = rangingSensor.measure(23, 24)
                    afterDistance = rangingSensor.measure(3, 4)
                    print("Before Distance : %.1f" % beforeDistance)
                    print("After Distance : %.1f" % afterDistance)

                    if(beforeDistance > 15 ):
                        # Walk forward
                        print(" Walk forward >>>>>")
                        motor.forward()
                    elif(beforeDistance < 15 and afterDistance > 15 ):
                        # Back off
                        print("Back off <<<<<")
                        motor.backward()
                    elif(beforeDistance < 15 and afterDistance < 15 ):
                        if(beforeDistance > afterDistance):
                            # Forward left
                            print("Forward left <<<<<")
                            motor.left()
                            motor.forward()
                        elif (beforeDistance <= afterDistance):
                            # Left rear back
                            print("Left rear back")
                            motor.left()
                            motor.backward()

                    time.sleep(2)
        except KeyboardInterrupt:
            motor.stop()


robotCar = Robot_Car()

robotCar.start()