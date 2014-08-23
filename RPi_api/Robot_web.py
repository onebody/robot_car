#!/usr/bin/env python
## coding=gbk
#
# Imports
import web
import RPi.GPIO as GPIO
from RobotMotor import RobotMotor
from RangingSensor import RangingSensor
from ServoAPI import  *

GPIO.setwarnings(False)

urls = (
    '/robot_api', 'index'
    )

print("Robot is running....")
rangingSensor = RangingSensor()

motor = RobotMotor()
motor.init(11, 12, 9, 15, 13, 7)

servoAPI = ServoAPI()
servoAPI.init()

servoPanAPI = ServoPanAPI()
servoPanAPI.init()

class index:
    distanceType_Before = 'Before'
    distanceType_After = 'After'

    isAuto = True

    delays = 0.5 #
    steps = 100 #

    def GET(self):
        i = web.input()
        action = i.action
        msg = ""

        if(action == 'go'):
            motor.forward()
            msg = "前进"
        elif(action == "back"):
            motor.backward()
            msg = "后退"
        elif(action == "stop"):
            motor.stop()
            servoAPI.stop()
            msg = "停止"
        elif(action == "b_d"):
            beforeDistance = rangingSensor.measure(16, 18)
            print("Before Distance : %.1f" % beforeDistance)
            msg = "前方距离:%.1f" % beforeDistance
        elif(action == "a_d"):
            afterDistance = rangingSensor.measure(19, 7)
            print("After Distance : %.1f" % afterDistance)
            msg = "后方距离:%.1f" % afterDistance
        elif(action == "t_l"):
            servoAPI.left()
            msg = "左转"
        elif(action == "t_r"):
            servoAPI.right()
            msg = "右转"
        elif(action == "t_m"):
            servoAPI.forward()
            msg = "回正"
        elif(action == "pt_m"):
            servoPanAPI.forward()
            msg = "回正"
        elif(action == "pt_l"):
            servoPanAPI.left()
            msg = "左探"
        elif(action == "pt_r"):
            servoPanAPI.right()
            msg = "右探"

        return "Hello, world!>>>" + action + "---" + unicode(msg, "gbk")

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()