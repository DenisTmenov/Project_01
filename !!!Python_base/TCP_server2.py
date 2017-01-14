#!/usr/bin/env python

from socket import *
import sqlite3 as lite
import pickle
from time import ctime


def search_workers_in_db(dec_data):
    conn = lite.connect('catalogDB.sqlite3')
    table = 'workers'  # table name in DB
    with conn:
        cursor = conn.cursor()
        # query for surname
        sql_select_worker_surname = (
            """SELECT name, surname FROM  '{}' WHERE surname LIKE '{}%'""".format(table, dec_data)
            )
        try:
            workers_surname = cursor.execute(sql_select_worker_surname)
            workers_surname = set(workers_surname.fetchall())
        except lite.OperationalError:
            print("...Error!")
        # query for name
        sql_select_worker_name = (
            """SELECT name, surname FROM  '{}' WHERE name LIKE '{}%'""".format(table, dec_data)
            )
        try:
            workers_name = cursor.execute(sql_select_worker_name)
            workers_name = set(workers_name.fetchall())
        except lite.OperationalError:
            print("...Error!")
    workers_surname.update(workers_name)  # sets combining
    workers_set = workers_surname             # combined sets
    if workers_set == set():
        workers_set = 'Nobody was founded'
        print(workers_set)
    else:
        print('...answer: ', workers_set)
    return workers_set


def get_worker_info(dec_data):
    conn = lite.connect('catalogDB.sqlite3')
    table = 'workers'  # table name in DB
    with conn:
        cursor = conn.cursor()
        sql_select_worker_info = (
            """SELECT name, surname, position, phone, email, fax, photo
               FROM '{}' WHERE name = '{}'""".format(table, dec_data)
        )
        try:
            worker_info = cursor.execute(sql_select_worker_info)
            worker_info = set(worker_info.fetchall())
        except lite.OperationalError:
            print("...Error!")
    print('...answer: ', worker_info)
    return worker_info


# def tuple_to_str(tup):
#     string = ''
#     for i in tup:
#         string += i
#     return string


host = ''
port = 8888
buf_size = 1024
addr = (host, port)

# Creating TCP/IP socket
tcp_ser_sock = socket(AF_INET, SOCK_STREAM)
# Binding the address(addr) with socket
tcp_ser_sock.bind(addr)
# Устанавливаем и запускаем приемник TCP
tcp_ser_sock.listen(1)

while True:
    print('waiting for connection...')

    # Accepting the client request for TCP connection
    tcp_client_sock, address = tcp_ser_sock.accept()
    print('...new connection from:', address, ctime())
    try:
        # while True:
            # receiving TCP message
            data = tcp_client_sock.recv(buf_size)
            # decoding data from client
            decoded_data = pickle.loads(data)
            print('...received:', decoded_data)

            if decoded_data:
                if decoded_data[0] == '#':
                    decoded_data = decoded_data[1:]
                    worker = get_worker_info(decoded_data)
                else:
                    worker = search_workers_in_db(decoded_data)
            else:
                worker = 'Nobody was founded'
            tcp_client_sock.send(pickle.dumps(worker))
            print('...send:{}'.format(worker), type(worker))
    except ConnectionResetError:
        print('...connection lost')
    # Закрываем соединение с клиентом
    tcp_client_sock.close()

# Строка никогда не выполняется (Закрытие сокета)
tcp_ser_sock.close()
