#!/usr/bin/env python3 

import socket

HOST = '127.0.0.1'
PORT = 17345

#create a socket object - use of 'with' saves a s.close() method
#AF_INET is IPv4 (addressfamily)
#SOCK_STREAM is TCP (transport protocol)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    s.bind((HOST, PORT)) #bind local interface and port
    s.listen() #let the socket listen on configured interface and port

    print('Server startet on port {}'.format(PORT))
    conn, addr = s.accept() #saving the connection as socket object and remote address as tuple into vars
    with conn:
        print('Connected by: {}'.format(addr))
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
