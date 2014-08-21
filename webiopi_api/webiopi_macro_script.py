# This version uses new-style automatic setup/destroy/mapping
# Need to change /etc/webiopi

# Imports
import webiopi
import time
import threading
import math
import smbus

# Retrieve GPIO lib
GPIO = webiopi.GPIO

# ===========================================================================
# Raspi_I2C Base Class
# ===========================================================================

class Raspi_I2C:
    def __init__(self, address, bus=smbus.SMBus(1), debug=False):
        self.address = address
        self.bus = bus
        self.debug = debug

    def reverseByteOrder(self, data):
        "Reverses the byte order of an int (16-bit) or long (32-bit) value"
        # Courtesy Vishal Sapre
        dstr = hex(data)[2:].replace('L', '')
        byteCount = len(dstr[::2])
        val = 0
        for i, n in enumerate(range(byteCount)):
            d = data & 0xFF
            val |= (d << (8 * (byteCount - i - 1)))
            data >>= 8
        return val

    def write8(self, reg, value):
        "Writes an 8-bit value to the specified register/address"
        try:
            self.bus.write_byte_data(self.address, reg, value)
            if (self.debug):
                print("I2C: Wrote 0x%02X to register 0x%02X" % (value, reg))
        except IOError as err:
            print("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1

    def writeList(self, reg, list):
        "Writes an array of bytes using I2C format"
        try:
            if (self.debug):
                print("I2C: Writing list to register 0x%02X:" % reg)
                print()
                list
            self.bus.write_i2c_block_data(self.address, reg, list)
        except IOError as err:
            print("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1

    def readList(self, reg, length):
        "Read a list of bytes from the I2C device"
        results = []
        try:
            results = self.bus.read_i2c_block_data(self.address, reg, length)
            if (self.debug):
                print("I2C: Device 0x%02X returned the following from reg 0x%02X" % (self.address, reg))
                print()
                results
            return results
        except IOError as err:
            print("Error accessing 09x%02X: Check your I2C address" % self.address)
            return -1

    def readU8(self, reg):
        "Read an unsigned byte from the I2C device"
        try:
            result = self.bus.read_byte_data(self.address, reg)
            if (self.debug):
                print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
            return result
        except IOError as  err:
            print("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1

    def readS8(self, reg):
        "Reads a signed byte from the I2C device"
        try:
            result = self.bus.read_byte_data(self.address, reg)
            if (self.debug):
                print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
            if (result > 127):
                return result - 256
            else:
                return result
        except IOError as  err:
            print("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1

    def readU16(self, reg):
        "Reads an unsigned 16-bit value from the I2C device"
        try:
            hibyte = self.bus.read_byte_data(self.address, reg)
            result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg + 1)
            if (self.debug):
                print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, result & 0xFFFF, reg))
            return result
        except IOError as  err:
            print("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1

    def readS16(self, reg):
        "Reads a signed 16-bit value from the I2C device"
        try:
            hibyte = self.bus.read_byte_data(self.address, reg)
            if (hibyte > 127):
                hibyte -= 256
            result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg + 1)
            if (self.debug):
                print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, result & 0xFFFF, reg))
            return result
        except IOError as err:
            print("Error accessing 0x%02X: Check your I2C address" % self.address)
            return -1


# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PWM:
    i2c = None

    # Registers/etc.
    __SUBADR1 = 0x02
    __SUBADR2 = 0x03
    __SUBADR3 = 0x04
    __MODE1 = 0x00
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09
    __ALLLED_ON_L = 0xFA
    __ALLLED_ON_H = 0xFB
    __ALLLED_OFF_L = 0xFC
    __ALLLED_OFF_H = 0xFD

    def __init__(self, address=0x60, debug=False):
        self.i2c = Raspi_I2C(address)
        self.address = address
        self.debug = debug
        if (self.debug):
            print ("Reseting PCA9685")
        self.i2c.write8(self.__MODE1, 0x00)

    def setPWMFreq(self, freq):
        "Sets the PWM frequency"
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        if (self.debug):
            print ("Setting PWM frequency to %d Hz" % freq)
            print ("Estimated pre-scale: %d" % prescaleval)
        prescale = math.floor(prescaleval + 0.5)
        if (self.debug):
            print ("Final pre-scale: %d" % prescale)

        oldmode = self.i2c.readU8(self.__MODE1);
        newmode = (oldmode & 0x7F) | 0x10             # sleep
        self.i2c.write8(self.__MODE1, newmode)        # go to sleep
        self.i2c.write8(self.__PRESCALE, int(math.floor(prescale)))
        self.i2c.write8(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.i2c.write8(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        "Sets a single PWM channel"
        self.i2c.write8(self.__LED0_ON_L + 4 * channel, on & 0xFF)
        self.i2c.write8(self.__LED0_ON_H + 4 * channel, on >> 8)
        self.i2c.write8(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
        self.i2c.write8(self.__LED0_OFF_H + 4 * channel, off >> 8)


class ServoAPI():
    pwm = PWM(0x6F, debug=True)

    servoMin = 150  # Min pulse length out of 4096
    servoMax = 600  # Max pulse length out of 4096
    servoMid = 350
    curServo = 0

    def left(self):
        if(self.curServo != self.servoMax):
            self.pwm.setPWM(0, 0, self.servoMax)
            self.curServo = self.servoMax

    def right(self):
        if(self.curServo != self.servoMin):
            self.pwm.setPWM(0, 0, self.servoMin)
            self.curServo = self.servoMin

    def forward(self):
        if(self.curServo != self.servoMid):
            self.pwm.setPWM(0, 0, self.servoMid)
            self.curServo = self.servoMid

    def stop(self):
        self.curServo = 0

    def init(self):
        self.pwm.setPWMFreq(60)
        self.curServo = 0


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
        pass

    #        GPIO.output(self.R1, GPIO.LOW)
    #        GPIO.output(self.R2, GPIO.HIGH)

    def right(self):
        pass

    #        GPIO.output(self.R1, GPIO.HIGH)
    #        GPIO.output(self.R2, GPIO.LOW)

    def stop(self):
        GPIO.output(self.L1, GPIO.LOW)
        GPIO.output(self.L2, GPIO.LOW)

    #        GPIO.output(self.R1, GPIO.LOW)
    #        GPIO.output(self.R2, GPIO.LOW)

    def forward(self):
        GPIO.output(self.L1, GPIO.HIGH)
        GPIO.output(self.L2, GPIO.LOW)

    def backward(self):
        GPIO.output(self.L1, GPIO.LOW)
        GPIO.output(self.L2, GPIO.HIGH)

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

#        GPIO.setFunction(self.R1, GPIO.OUT)
#        GPIO.setFunction(self.R2, GPIO.OUT)


class Robot_Car(threading.Thread):
    distanceType_Before = 'Before'
    distanceType_After = 'After'

    rangingSensor = RangingSensor()

    motor = RobotMotor()

    isAuto = True

    delays = 0.5 #
    steps = 100 #

    def __init__(self):
        threading.Thread.__init__(self)

    def stop(self):
        self.isAuto = False
        self.motor.stop()

    def run(self):
        while not self.isAuto:
            # Before Distance
            beforeDistance = self.rangingSensor.measure(23, 24)
            afterDistance = self.rangingSensor.measure(3, 4)
            print("Before Distance : %.1f" % beforeDistance)
            print("After Distance : %.1f" % afterDistance)
            if(beforeDistance > 15 ):
                # Walk forward
                print(" Walk forward >>>>>")
                self.motor.forward()
            elif(beforeDistance < 15 and afterDistance > 15 ):
                # Back off
                print("Back off <<<<<")
                self.motor.backward()
            elif(beforeDistance < 15 and afterDistance < 15 ):
                if(beforeDistance > afterDistance):
                    # Forward left
                    print("Forward left <<<<<")
                    self.motor.left()
                    self.motor.forward()
                elif (beforeDistance <= afterDistance):
                    # Left rear back
                    print("Left rear back")
                    self.motor.right()
                    self.motor.backward()
            time.sleep(2)

# ------    ------------------------------------- #
# Macro     ion part                              #
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

robotMotor = RobotMotor()

robotCar = Robot_Car()
Thread = Robot_Car()

servoAPI = ServoAPI()
servoAPI.init()


@webiopi.macro
def robotMotor_setup(L1, L2, LS, R1, R2, RS):
    robotMotor.init(int(L1), int(L2), int(LS), int(R1), int(R2), int(RS))


@webiopi.macro
def robotMotor_control(action):
    robotCar.stop()
    if(action == 'forward'):
        robotMotor.forward()
    elif (action == 'backward'):
        robotMotor.backward()
    elif(action == 'turn_left_forward'):
    #        robotMotor.left()
        servoAPI.left()
    #        robotMotor.forward()
    elif(action == 'turn_right_forward'):
    #        robotMotor.right()
        servoAPI.right()
    #        robotMotor.forward()
    elif(action == 'turn_mid'):
        servoAPI.forward()
    elif(action == 'stop'):
        robotMotor.stop()
    elif(action == 'auto'):
        Thread.start()
    elif(action == 'auto_stop'):
        Thread._stop()


# Called by WebIOPi at script loading
def setup():
    print("")
    # init()

    #    set_speed(0.5)
    # stop()


# Called by WebIOPi at server shutdown
def destroy():
    # Reset GPIO functions
    robotMotor.stop()

    webcamStepMotor.destroy()


