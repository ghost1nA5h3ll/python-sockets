#! /usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 17345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'hello my server')
    data = s.recv(1024)

print('Received from server: {}'.format(repr(data)))

