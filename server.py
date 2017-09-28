#!/usr/bin/env python3
"""
    Server.py - Chat app server
    Authors:
        - Hoanh An (hoanhan@bennington.edu)
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Dung Le (dungle@bennington.edu)
    Date: 09/26/17
"""

import threading
import time
import socket

TCP_ADDRESS = '0.0.0.0'
TCP_PORT = 9000
BUFFER_SIZE = 1024

CLIENTS = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((TCP_ADDRESS, TCP_PORT))

class TimeThread(threading.Thread):

    def __init__(self, thread_id, name):

        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def connect(self):
        while True:
            #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.bind((TCP_ADDRESS, TCP_PORT))
            
            s.listen(1)

            conn, addr = s.accept()
            CLIENTS[conn] = addr[0]
            print('Connection address: {0}'.format(addr[0]))

            data = conn.recv(BUFFER_SIZE).decode()
            sender = CLIENTS[conn]
            while data != "":
                print("received data: {0}".format(data))
                #conn.send(data.encode())
                for client in CLIENTS:
                    #print(client)
                    #client.send(sender.encode())
                    #client.send(data.encode())
                    message = '>> {0} : {1}'.format(sender, data)
                    client.send(message.encode())
                    print('Sent data to {0}'.format(CLIENTS[client]))
#                print('Sent data: {0}'.format(data))
                data = conn.recv(BUFFER_SIZE).decode()
                print('New data: {0}'.format(data))

            conn.close()

        #s.close()

    def run(self):
        print('Starting {0}'.format(self.name))
        self.connect()
        print('Finishing {0}'.format(self.name))


thread_lock = threading.Lock()
threads = []

thread_1 = TimeThread(1, "thread_1")
thread_2 = TimeThread(2, "thread_2")
thread_3 = TimeThread(3, "thread_3")

thread_1.start()
thread_2.start()
thread_3.start()

threads.append(thread_1)
threads.append(thread_2)
threads.append(thread_3)

for thread in threads:
	thread.join()

sock.close()
