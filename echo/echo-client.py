#! /usr/bin/env python3

import socket

#configure target IP and port
HOST = '127.0.0.1' 
PORT = 17345

#create a socket object (IPv4 with TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) #connect to echo-server
    s.sendall(b'hello my server') #send data to server
    data = s.recv(1024) #get answer from server

print('Received from server: {}'.format(repr(data))) #print the data to the commandline

