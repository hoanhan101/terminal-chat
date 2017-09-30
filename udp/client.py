#!/usr/bin/env python3

"""
    client.py - TCP Chat app client
    Authors:
    - Hoanh An (hoanhan@bennington.edu)
    - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
    - Dung Le (dungle@bennington.edu)
    Date: 09/29/17
"""

import socket
import threading

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class ClientThread(threading.Thread):
    def __init__(self, thread_id, function):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.function = function

    def send(self):
        print('Welcome to our UDP chat.')
        username = input('To get started, please provide a username: ')
        username = '@' + username
        s.sendto(username.encode(), (MCAST_GRP, MCAST_PORT))
        
        while True:
            MESSAGE = input(">> ")

            # broadcast our message to the world
            s.sendto(MESSAGE.encode(), (MCAST_GRP, MCAST_PORT))
            print("SENT {0} TO {1}".format(MESSAGE, MCAST_GRP))

    def receive(self):
        while True:
            data, addr = s.recvfrom(1024)
            data = data.decode()
            print("RECEIVED {0} FROM {1}".format(data, addr[0]))

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
