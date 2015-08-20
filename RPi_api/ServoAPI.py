# /usr/bin/python

from Raspi_PWM_Servo_Driver import PWM


class ServoAPI():
    debug = False
    pwm = None

    servoMin = 150  # Min pulse length out of 4096
    servoMax = 550  # Max pulse length out of 4096
    servoMid = 350
    curServo = 0

    def __init__(self, debug=False):
        self.debug = debug
        self.pwm = PWM(0x6F, debug=False)

    def left(self):
        if (self.curServo != self.servoMax):
            self.pwm.setPWM(0, 0, self.servoMax)
            self.curServo = self.servoMax

    def right(self):
        if (self.curServo != self.servoMin):
            self.pwm.setPWM(0, 0, self.servoMin)
            self.curServo = self.servoMin

    def forward(self):
        if (self.curServo != self.servoMid):
            self.pwm.setPWM(0, 0, self.servoMid)
            self.curServo = self.servoMid

    def stop(self):
        self.pwm.setPWM(0, 0, 0)
        self.curServo = 0

    def init(self):
        self.pwm.setPWMFreq(60)
        self.curServo = 0


class ServoPanAPI():
    debug = False
    pwm = None

    servoMin = 150  # Min pulse length out of 4096
    servoMax = 550  # Max pulse length out of 4096
    servoMid = 350
    curServo = 0

    def __init__(self, debug=False):
        self.debug = debug
        self.pwm = PWM(0x6F, debug=False)

    def left(self):
        if (self.curServo != self.servoMax):
            self.pwm.setPWM(15, 0, self.servoMax)
            self.curServo = self.servoMax

    def right(self):
        if (self.curServo != self.servoMin):
            self.pwm.setPWM(15, 0, self.servoMin)
            self.curServo = self.servoMin

    def forward(self):
        if (self.curServo != self.servoMid):
            self.pwm.setPWM(15, 0, self.servoMid)
            self.curServo = self.servoMid

    def stop(self):
        self.pwm.setPWM(15, 0, 0)
        self.curServo = 0

    def init(self):
        self.pwm.setPWMFreq(60)
        self.curServo = 0

#
# servoAPI = ServoAPI(True)
# servoAPI = ServoPanAPI(True)
#servoAPI.init()
#while (True):
#    print(" turn left>>>>")
#    servoAPI.left()
#    time.sleep(2)
#    print(" mid >>>>")
#    servoAPI.forward()
#    time.sleep(2)
#    print(" turn right>>>>")
#    servoAPI.right()
#    time.sleep(2)
#    print(" mid >>>>")
#    servoAPI.forward()
#    time.sleep(2)

