#!/usr/bin/env python

from socket import *
from time import ctime

from Robot_auto import *


robot_car = Robot_Car()


def process(data):
    robot_car.manual(data)


class RobotServer():
    HOST = ''
    PORT = 47788
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    tcpSerSock = socket(AF_INET, SOCK_STREAM)

    robot_car = Robot_Car()

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
                        data = data.replace("\r", '').replace("\n", '')
                        print ('Received from client:', data)
                        print(" new thread exec 1...")
                        thread.start_new_thread(process, (data,))
                        # self.process(data)
                        print ('Received from client111:', data)
                        tcpCliSock.send('[%s] %s' % (ctime(), data))
                        print ('Received from client222:', data)
                except:
                    break

            tcpCliSock.close()
            print (addr, ' this connection closed! ')

        self.tcpSerSock.close()
        print ('Robot Server connection closed! ')


if __name__ == "__main__":
    print("Robot Socket server is running....")
    robotServer = RobotServer("", 47788, 5)
    robotServer.start()