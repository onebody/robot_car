#!/usr/bin/python
# This version uses new-style automatic setup/destroy/mapping
# Need to change /etc/webiopi

# Imports
import RPi.GPIO as GPIO
import time
from RobotMotor import RobotMotor
from RangingSensor import RangingSensor
from ServoAPI import *

GPIO.setwarnings(False)

class Robot_Car():
    distanceType_Before = 'Before'
    distanceType_After = 'After'

    isAuto = True

    delays = 0.5  #
    steps = 100  #

    rangingSensor = RangingSensor()

    motor = RobotMotor()
    motor.init(11, 12, 9, 15, 13, 7)

    servoAPI = ServoAPI()
    servoAPI.init()

    servoPanAPI = ServoPanAPI()
    servoPanAPI.init()

    def stop(self):
        self.isAuto = False

    def start(self):
        print("Robot is running....")

        print("RobotMotor is inited")
        try:
            while True:
                print("in Thread")
                if (self.isAuto == True):
                    print("in Thread>>>>>")
                    # Before Distance
                    beforeDistance = self.rangingSensor.measure(16, 18)
                    afterDistance = self.rangingSensor.measure(19, 7)
                    print("Before Distance : %.1f" % beforeDistance)
                    print("After Distance : %.1f" % afterDistance)

                    if (beforeDistance > 15 ):
                        # Walk forward
                        print(" Walk forward >>>>>")
                        self.motor.forward()
                    elif (beforeDistance < 15 and afterDistance > 15 ):
                        # Back off
                        print("Back off <<<<<")
                        self.servoAPI.forward()
                        self.motor.backward()
                    elif (beforeDistance < 15 and afterDistance < 15 ):
                        if (beforeDistance < 5 and afterDistance < 5 ):
                            self.motor.stop()
                        else:
                            if (beforeDistance > afterDistance):
                                # Forward left
                                print("Forward left <<<<<")
                                # motor.left()
                                self.servoAPI.left()
                                self.motor.forward()
                            elif (beforeDistance <= afterDistance):
                                # Left rear back
                                print("Left rear back")
                                # motor.left()
                                self.servoAPI.right()
                                self.motor.backward()
                    time.sleep(1)
                else:
                    break
        except KeyboardInterrupt:
            self.servoAPI.forward()
            self.servoAPI.stop()
            self.servoPanAPI.forward()
            self.servoPanAPI.stop()
            self.motor.stop()


    def manual(self, action):
        msg = ""
        if (action == 'go'):
            self.motor.forward()
        elif (action == "back"):
            self.motor.backward()
        elif (action == "stop"):
            self.motor.stop()
            self.servoAPI.stop()
            self.servoPanAPI.stop()
        elif (action == "b_d"):
            beforeDistance = self.rangingSensor.measure(16, 18)
            print("Before Distance : %.1f" % beforeDistance)
        elif (action == "a_d"):
            afterDistance = self.rangingSensor.measure(19, 7)
            print("After Distance : %.1f" % afterDistance)
        elif (action == "t_l"):
            self.servoAPI.left()
        elif (action == "t_r"):
            self.servoAPI.right()
        elif (action == "t_m"):
            self.servoAPI.forward()
        elif (action == "pt_m"):
            self.servoPanAPI.forward()
        elif (action == "pt_l"):
            self.servoPanAPI.left()
        elif (action == "pt_r"):
            self.servoPanAPI.right()
        elif (action == "auto"):
            self.start()
        elif (action == "auto_stop"):
            self.stop()
