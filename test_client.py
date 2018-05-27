#!/usr/bin/env python

import socket


TCP_IP = socket.gethostname()#'10.128.0.2'#'35.196.99.240'##"
print (TCP_IP)
TCP_PORT = 5001
BUFFER_SIZE = 20
MESSAGE = '1.32136 103.76038   '

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(MESSAGE.encode('utf-8'))
print('Sended!')
#data = s.recv(BUFFER_SIZE)

#print("received data:" + str(data))

s.close()
print('Finished!!')
