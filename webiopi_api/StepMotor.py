__author__ = 'onebody'

# Imports
import webiopi
import time

# Retrieve GPIO lib
GPIO = webiopi.GPIO

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
