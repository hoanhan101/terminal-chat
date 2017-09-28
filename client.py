#!/usr/bin/env python3
"""
    client.py - Chat app client
    Authors:
        - Hoanh An (hoanhan@bennington.edu)
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Dung Le (dungle@bennington.edu)
    Date: 09/26/17
"""

import socket

#TCP_ADDRESS = '127.0.0.1'
#
#TCP_PORT = 9000
#
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#s.connect((TCP_ADDRESS, TCP_PORT))
#
#while True:
#    MESSAGE = input("input: ")        # the message to send to the server
#    s.send(MESSAGE.encode())
#    print('Sent {0} to {1}'.format(MESSAGE, TCP_ADDRESS))
#
#s.close()

import threading
import time
import socket

TCP_ADDRESS = '127.0.0.1'
#TCP_ADDRESS = '10.241.32.238'
TCP_PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TCP_ADDRESS, TCP_PORT))

class TimeThread(threading.Thread):

    def __init__(self, thread_id, name, function):

        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.function = function

    def send(self):
        while True:
            #MESSAGE = input("input: ")        # the message to send to the server
            MESSAGE = input("")
            s.send(MESSAGE.encode())
            #print('Sent {0} to {1}'.format(MESSAGE, TCP_ADDRESS))

        s.close()

    def receive(self):
        while True:
            #client = s.recv(1024).decode()
            data = s.recv(1024).decode()
            #print('receieved data 1: {0}'.format(data))

            if data != "":
                #print('>> {1} : {0}'.format(data,client))
                print(data)
                #data = s.recv(1024).decode()
                #print('receieved data 2: {0}'.format(data))

        #s.close()

    def run(self):
        print('Starting {0}'.format(self.name))
        if self.function == "send":
            self.send()
        elif self.function == "receive":
            self.receive()
        print('Finishing {0}'.format(self.name))


# thread_lock = threading.Lock()
# threads = []
#
# thread_1 = TimeThread(1, "thread_1")
# thread_2 = TimeThread(2, "thread_2")
thread_3 = TimeThread(3, "thread_3", "receive")
thread_4 = TimeThread(4, "thread_4", "send")
#
# thread_1.start()
# thread_2.start()
thread_3.start()
thread_4.start()
#
# threads.append(thread_1)
# threads.append(thread_2)
# threads.append(thread_3)
#
# for thread in threads:
#     thread.join()

