#!/usr/bin/env python3
"""
    client.py - TCP Chat app client
    Authors:
        - Hoanh An (hoanhan@bennington.edu)
        - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
        - Dung Le (dungle@bennington.edu)
    Date: 09/26/17
"""

import threading
import time
import socket

#TCP_ADDRESS = '127.0.0.1'
TCP_ADDRESS = '10.10.241.85'
TCP_PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TCP_ADDRESS, TCP_PORT))

class ClientThread(threading.Thread):

    def __init__(self, thread_id, function):

        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.function = function

    def send(self):
        while True:
            MESSAGE = input("")
            s.send(MESSAGE.encode())
            #print('Sent {0} to {1}'.format(MESSAGE, TCP_ADDRESS))

        s.close()

    def receive(self):
        while True:
            data = s.recv(1024).decode()

            if data != "":
                print(data)

        s.close()

    def run(self):
        print('Starting Thread {0}'.format(self.thread_id))
        
        if self.function == "SEND":
            self.send()
        elif self.function == "RECEIVE":
            self.receive()
        
        print('Finishing Thread {0}'.format(self.thread_id))

thread_1 = ClientThread(1, "RECEIVE")
thread_2 = ClientThread(2, "SEND")
thread_1.start()
thread_2.start()

