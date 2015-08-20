#!/usr/bin/env python

from socket import *
# from time import ctime
# import thread


print("A Socket server is running....")
curPort = 47799

class RobotServer():
    HOST = ''
    PORT = 47799
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    tcpSerSock = socket(AF_INET, SOCK_STREAM)

    def __init__(self, host="", port=PORT, client_count=5):
        self.tcpSerSock.bind((host, port))
        self.tcpSerSock.listen(client_count)


    def process(self,data):
        print data


    def to(self, tcpCliSock):
        data = tcpCliSock.recv(self.BUFSIZE)
        if not data:
            return
        elif data == "bye":
            tcpCliSock.send('bye')
            return
        else:
            data = data.replace("\r", '').replace("\n", '')
            print ('1 Received from client:', data)
            # thread.start_new_thread(process, (data,))
            self.process(data)
            print ('1 send to client:', data)
            #tcpCliSock.send('[%s] %s' % (ctime(), data))

    def start(self):
        while True:
            print ('Waiting for connection...')
            tcpCliSock, addr = self.tcpSerSock.accept()
            print ('...connected from: ', addr)

            while True:
                try:
                    self.to(tcpCliSock)
                    break
                except IOError, error:
                    print(" exit>>>")
                    print(error)
                    print(" exit<<<<<")
                    break

            tcpCliSock.close()
            print ('this connection closed! ')

        self.tcpSerSock.close()
        print ('server connection closed! ')


if __name__ == "__main__":
    robotServer = RobotServer("", curPort, 5)
    robotServer.start()
