#!/usr/bin/env python

from socket import *
from time import ctime

from Robot_auto import *

print("Robot Socket server is running....")
robot_car = Robot_Car()


class RobotServer():
    HOST = ''
    PORT = 47788
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    tcpSerSock = socket(AF_INET, SOCK_STREAM)

    def __init__(self, host="", port=47788, client_count=5):
        self.tcpSerSock.bind((host, port))
        self.tcpSerSock.listen(client_count)

    def start(self):
        while True:
            print ('Waiting for connection...')
            tcpCliSock, addr = self.tcpSerSock.accept()
            print ('...connected from: ', addr)

            while True:
                try:
                    data = tcpCliSock.recv(self.BUFSIZE)
                    if not data:
                        break
                    elif data == "bye":
                        tcpCliSock.send('bye')
                        break
                    else:
                        robot_car.manual(data)
                        print ('Received from client:', data)
                        tcpCliSock.send('[%s] %s' % (ctime(), data))
                except:
                    break

            self.tcpCliSock.close()
            print ('connection closed! ')

        self.tcpSerSock.close()
        print ('connection closed! ')


if __name__ == "__main__":
    robotServer = RobotServer("", 47788, 5)
    robotServer.start()