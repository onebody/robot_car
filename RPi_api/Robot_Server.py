#!/usr/bin/env python

from socket import *
# from time import ctime

from Robot_auto import *


print("Robot Socket server is running....")
robot_car = Robot_Car(debug=False)


def process(data):
    robot_car.manual(data)


class RobotServer():
    HOST = ''
    PORT = 47788
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    tcpSerSock = socket(AF_INET, SOCK_STREAM)

    def __init__(self, host="", port=47788, client_count=5):
        self.tcpSerSock.bind((host, port))
        self.tcpSerSock.listen(client_count)

    def goto(self, tcpCliSock):
        data = tcpCliSock.recv(self.BUFSIZE)
        data = data.replace("\r", '').replace("\n", '')
        print ('1.Received from client:', data)

        if not data:
            return
        elif data == "bye":
            tcpCliSock.send(data)
            return
        else:
            print (" Robot Server call RPi...")
            thread.start_new_thread(process, (data,))
            # robot_car.manual(data)
            # print ('1 send to client:', data)
            # tcpCliSock.send('[%s] %s' % (ctime(), data))

    def start(self):
        while True:
            print ('Waiting for connection...')
            tcpCliSock, addr = self.tcpSerSock.accept()
            print ('...connected from: ', addr)

            while True:
                try:
                    self.goto(tcpCliSock)
                    break
                except IOError, error:
                    # print(" exit>>>")
                    # print(error)
                    # print(" exit<<<<<")
                    print (" Robot Server call RPi...end")
                    break

            tcpCliSock.close()
            print ('this connection closed! ')

        self.tcpSerSock.close()
        print ('server connection closed! ')


if __name__ == "__main__":
    robotServer = RobotServer("", 47788, 5)
    robotServer.start()