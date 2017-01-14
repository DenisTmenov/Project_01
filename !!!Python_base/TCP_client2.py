#!/usr/bin/env python

from socket import *
import pickle

host = '127.0.0.1'
port = 8888
buf_size = 1024
addr = (host, port)


while True:
    data = input('NickName > ')
    if not data:
        continue
    else:
        tcp_client_sock = socket(AF_INET, SOCK_STREAM)
        tcp_client_sock.connect(addr)
        tcp_client_sock.send(pickle.dumps(data))

    data = tcp_client_sock.recv(buf_size)
    data = pickle.loads(data)
    if data == set():
        print('Worker not found')
    else:
        print(data)

    tcp_client_sock.close()
