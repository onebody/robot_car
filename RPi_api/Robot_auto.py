#!/usr/bin/python
# This version uses new-style automatic setup/destroy/mapping
# Need to change /etc/webiopi

# Imports
import RPi.GPIO as GPIO
import time
from RobotMotor import RobotMotor
from RangingSensor import RangingSensor
from ServoAPI import  ServoAPI

GPIO.setwarnings(False)

class Robot_Car():
    distanceType_Before = 'Before'
    distanceType_After = 'After'

    isAuto = True

    delays = 0.5 #
    steps = 100 #

    def stop(self):
        self.isAuto = False

    def start(self):
        print("Robot is running....")
        rangingSensor = RangingSensor()

        motor = RobotMotor()
        motor.init(11, 12, 9, 15, 13, 7)

        servoAPI = ServoAPI()
        servoAPI.init()

        print("RobotMotor is inited")
        try:
            while True:
                print("in Thread")
                if(self.isAuto == True):
                    print("in Thread>>>>>")
                    # Before Distance
                    beforeDistance = rangingSensor.measure(16, 18)
                    afterDistance = rangingSensor.measure(19, 7)
                    print("Before Distance : %.1f" % beforeDistance)
                    print("After Distance : %.1f" % afterDistance)

                    if(beforeDistance > 15 ):
                        # Walk forward
                        print(" Walk forward >>>>>")
                        motor.forward()
                    elif(beforeDistance < 15 and afterDistance > 15 ):
                        # Back off
                        print("Back off <<<<<")
                        servoAPI.forward()
                        motor.backward()
                    elif(beforeDistance < 15 and afterDistance < 15 ):
                        if(beforeDistance < 5 and afterDistance < 5 ):
                            motor.stop()
                        else:
                            if(beforeDistance > afterDistance):
                                # Forward left
                                print("Forward left <<<<<")
                                #                                motor.left()
                                servoAPI.left()
                                motor.forward()
                            elif (beforeDistance <= afterDistance):
                                # Left rear back
                                print("Left rear back")
                                #                                motor.left()
                                servoAPI.right()
                                motor.backward()

                    time.sleep(2)
        except KeyboardInterrupt:
            GPIO.cleanup()
            servoAPI.stop()


robotCar = Robot_Car()

robotCar.start()