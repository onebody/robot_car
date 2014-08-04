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
    ports = [8, 11, 25, 2]

    def turnWebcam(self, steps_str, clockwise_str, delay):
        steps = int(steps_str)

        clockwise = int(clockwise_str)

        arr = [0, 1, 2, 3]

        if clockwise != 1:
            arr = [3, 2, 1, 0]

        ports = self.ports

        #for p in ports:
        #    GPIO.setFunction(p, GPIO.OUT)

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
        for p in self.ports:
            GPIO.setFunction(p, GPIO.OUT)

    def destroy(self):
        for p in self.ports:
            GPIO.setFunction(p, GPIO.IN)

# -------------------------------------------------- #
# Constants definition                               #
# -------------------------------------------------- #

# Left motor GPIOs
L1 = 22 # H-Bridge 1
L2 = 27 # H-Bridge 2
LS = 7 # H-Bridge 1,2EN

# Right motor GPIOs
R1 = 17 # H-Bridge 3
R2 = 18 # H-Bridge 4
RS = 9 # H-Bridge 3,4EN

# -------------------------------------------------- #
# Convenient PWM Function                            #
# -------------------------------------------------- #

# Set the speed of two motors
def set_speed(speed):
    GPIO.pulseRatio(LS, speed)
    GPIO.pulseRatio(RS, speed)

# -------------------------------------------------- #
# Left Motor Functions                               #
# -------------------------------------------------- #

def left_stop():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.LOW)


def left_forward():
    GPIO.output(L1, GPIO.HIGH)
    GPIO.output(L2, GPIO.LOW)


def left_backward():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.HIGH)

# -------------------------------------------------- #
# Right Motor Functions                              #
# -------------------------------------------------- #
def right_stop():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.LOW)


def right_forward():
    GPIO.output(R1, GPIO.HIGH)
    GPIO.output(R2, GPIO.LOW)


def right_backward():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.HIGH)

# -------------------------------------------------- #
# Macro definition part                              #
# -------------------------------------------------- #
rangingSensor = RangingSensor()

@webiopi.macro
def rangingSensor_Distance(GPIO_TRIGGER, GPIO_ECHO):
    return rangingSensor.measure(int(GPIO_TRIGGER), int(GPIO_ECHO))


webcamStepMotor = StepMotor()

@webiopi.macro
def webcamStepMotor_turnWebcam( steps_str, clockwise_str, delay):
    return webcamStepMotor.turnWebcam(steps_str, clockwise_str, delay)


@webiopi.macro
def webcamStepMotor_setup( in1, in2, in3, in4):
    return webcamStepMotor.setup(in1, in2, in3, in4)


@webiopi.macro
def go_forward():
    init()
    left_forward()
    right_forward()


@webiopi.macro
def go_backward():
    init()
    left_backward()
    right_backward()


@webiopi.macro
def turn_left():
    init()
    left_backward()
    right_forward()


@webiopi.macro
def turn_right():
    init()
    left_forward()
    right_backward()


@webiopi.macro
def stop():
    init()
    left_stop()
    right_stop()


def init():
# Setup GPIOs
#    GPIO.setFunction(LS, GPIO.PWM)
    GPIO.setFunction(L1, GPIO.OUT)
    GPIO.setFunction(L2, GPIO.OUT)

    #    GPIO.setFunction(RS, GPIO.PWM)
    GPIO.setFunction(R1, GPIO.OUT)
    GPIO.setFunction(R2, GPIO.OUT)

# Called by WebIOPi at script loading
def setup():
    print("")
    # init()

    #    set_speed(0.5)
    # stop()


# Called by WebIOPi at server shutdown
def destroy():
# Reset GPIO functions
#    GPIO.setFunction(LS, GPIO.IN)
    GPIO.setFunction(L1, GPIO.IN)
    GPIO.setFunction(L2, GPIO.IN)

    #    GPIO.setFunction(RS, GPIO.IN)
    GPIO.setFunction(R1, GPIO.IN)
    GPIO.setFunction(R2, GPIO.IN)

    webcamStepMotor.destroy()


