#!/usr/bin/env python

from socket import *
from time import ctime

HOST = ''
PORT = 4700
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print 'Waiting for connection...'
    tcpCliSock, addr = tcpSerSock.accept()
    print '...connected from: ', addr

    while True:
        try:
            data = tcpCliSock.recv(BUFSIZE)
            if not data:
                break
            elif data == "bye":
                tcpCliSock.send('bye')
                break
            else:
                print 'Received from client:', data
                tcpCliSock.send('[%s] %s' % (ctime(), data))
        except:
            break

    tcpCliSock.close()

tcpSerSock.close()