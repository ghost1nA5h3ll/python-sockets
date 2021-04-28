#! /usr/bin/env python3

import socket,selectors,types

#custom functions / classes

def accept_request(soc):
    conn, addr = soc.accept() #save socket object into conn and remote address tuple into addr
    print('<accepted connection> {}'.format(addr)) #print something to visualize
    conn.setblocking(False) #dont block - be ready for multiple connections
    data = types.SimpleNamespace(addr=addr,inb=b'', outb=b'') #save data as SimpleNamespace object
    events = selectors.EVENT_READ | selectors.EVENT_WRITE #set events to register to selectors
    sel.register(conn, events, data=data) #register socket, events and data

def handle_connection(key, mask):
    soc = key.fileobj
    data = key.data

    #if there are read events the socket receive the data
    if mask & selectors.EVENT_READ:
        recv_data = soc.recv(1024)
        if recv_data:
            data.outb += recv_data #save the received data to echo later
        else:
            print('<closing connection> {}'.format(data.addr))
            sel.unregister(soc) #unregister socket from selectors
            soc.close() #close the socket object
    
    #if there are write events the socket echos the received data via socket to client
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('<echoing> {} to {}'.format(repr(data.outb), data.addr))
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:] #remove the already send data from the "buffer"


#configure interface and port as tuple
server_config = ('127.0.0.1', 34516)

#create selectors object
sel = selectors.DefaultSelector()

#create socket object. IPv4 with TCP
lsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsoc.bind(server_config)
lsoc.listen()
print('Server is listening on: {}'.format(server_config))
lsoc.setblocking(False) #configure non-blocking mode 

#register socket to selectors object -> read event data and save values into data var
sel.register(lsoc, selectors.EVENT_READ, data=None)

while True:
    events = sel.select(timeout=None) #reading data from the registered socket and save to events var

    #loop through all selected event tuples
    for key, mask in events:
        if key.data is None:
            #if key.data is None we need to accept the connection and get socketobjects
            accept_request(key.fileobj)
        else:
            #otherwise the connection is already established we need to receive data 
            handle_connection(key, mask)
