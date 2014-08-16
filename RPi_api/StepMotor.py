#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

class StepMotor():
    ports = [24, 23, 22, 26]

    def turnWebcam(self, steps_str, clockwise_str, delay):
        steps = int(steps_str)

        clockwise = int(clockwise_str)

        arr = [0, 1, 2, 3]

        if clockwise != 1:
            arr = [3, 2, 1, 0]

        ports = self.ports

        GPIO.setmode(GPIO.BOARD)
        for p in ports:
            GPIO.setup(p, GPIO.OUT)

        for x in range(0, steps):
            for j in arr:
                time.sleep(float(delay))

                for i in range(0, 4):
                    if i == j:
                        GPIO.output(ports[i], False)

                    else:
                        GPIO.output(ports[i], True)


    def setup(self, in1, in2, in3, in4):
        self.ports = [int(in1), int(in2), int(in3), int(in4)]

    def destroy(self):
        GPIO.setmode(GPIO.BOARD)
        for p in self.ports:
            GPIO.setup(p, GPIO.IN)