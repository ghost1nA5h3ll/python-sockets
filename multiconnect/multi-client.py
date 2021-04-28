#! /usr/bin/env python3

import socket,selectors,types,sys

sel = selectors.DefaultSelector()
messages = [b'This is mesage No. 1 from the client', b'Hey! here comes message No. 2 from the client']

def start_connections(host, port, num_conn):
    server_addr = (host, port)
    for i in range(0, num_conn):
        conn_id = i+1 #creating a connection id for identification 
        print('>> starting connection {} to server {}'.format(conn_id, server_addr))
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket object (IPv4 with TCP)
        soc.setblocking(False) #dont block 
        soc.connect_ex(server_addr) #connect_ex wont raise a BlockingIOError Exception
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=conn_id,msg_total=sum(len(m) for m in messages), recv_total=0, messages=list(messages),outb=b'')
        sel.register(soc, events, data=data)

def handle_connection(key, mask):
    soc = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = soc.recv(1024)
        if recv_data:
            print('<< received: {} from connection {}'.format(repr(recv_data), data.connid))
            data.recv_total += len(recv_data) #track how much data got received
        #if there is no data received or the end of the data is reached
        if not recv_data or data.msg_total == data.recv_total:
            print('<closing connection> {}'.format(data.connid))
            sel.unregister(soc)
            soc.close()
    #if there are write events
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0) #put the first element of messages into data.outb if data.outb is empty
        if data.outb:
            print('>> sending {} to connection {}'.format(repr(data.outb), data.connid))
            sent = soc.send(data.outb) #send data in outb ("buffer")
            data.outb = data.outb[sent:] #clear buffer

if len(sys.argv) != 4:
    print("usage: {} <host> <port> <num_connections>".format(sys.argv[0]))
    sys.exit(1)

host, port, num_conn = sys.argv[1:4]

start_connections(host, int(port), int(num_conn))

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key,mask in events:
                handle_connection(key, mask)
        if not sel.get_map():
            break
except:
    print('EXITING! Keyboard interrupt...')
finally:
    sel.close()