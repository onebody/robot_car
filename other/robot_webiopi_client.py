# This version uses new-style automatic setup/destroy/mapping
# Need to change /etc/webiopi

from webiopi.clients import *
from time import sleep

# Create a WebIOPi client
client = PiHttpClient("192.168.1.103")
#client = PiMixedClient("192.168.1.234")
#client = PiCoapClient("192.168.1.234")
#client = PiMulticastClient()

client.setCredentials("webiopi", "webiopi")

# RPi native GPIO
GPIO = NativeGPIO(client)

# -------------------------------------------------- #
# Constants definition                               #
# -------------------------------------------------- #

# Left motor GPIOs
L1 = 22 # H-Bridge 1
L2 = 27 # H-Bridge 2
LS = 21 # H-Bridge 1,2EN

# Right motor GPIOs
R1 = 17 # H-Bridge 3
R2 = 18 # H-Bridge 4
RS = 25 # H-Bridge 3,4EN

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
def go_forward():
    left_forward()
    right_forward()


def go_backward():
    left_backward()
    right_backward()


def turn_left():
    left_backward()
    right_forward()


def turn_right():
    left_forward()
    right_backward()


def stop():
    left_stop()
    right_stop()

# Called by WebIOPi at script loading
def setup():
    # Setup GPIOs
    #GPIO.setFunction(LS, GPIO.PWM)
    GPIO.setFunction(L1, GPIO.OUT)
    GPIO.setFunction(L2, GPIO.OUT)

    #GPIO.setFunction(RS, GPIO.PWM)
    GPIO.setFunction(R1, GPIO.OUT)
    GPIO.setFunction(R2, GPIO.OUT)

    #set_speed(0.5)
    stop()


# Called by WebIOPi at server shutdown
def destroy():
    # Reset GPIO functions
    #GPIO.setFunction(LS, GPIO.IN)
    GPIO.setFunction(L1, GPIO.IN)
    GPIO.setFunction(L2, GPIO.IN)

    #GPIO.setFunction(RS, GPIO.IN)
    GPIO.setFunction(R1, GPIO.IN)
    GPIO.setFunction(R2, GPIO.IN)


# Temperature sensor named "temp0"
temp = Temperature(client, "temp0")

#while True:
# Retrieve temperature
t = temp.getCelsius()
print("Temperature = %.2f Celsius" % t)

sleep(1)

go_forward()
stop()
