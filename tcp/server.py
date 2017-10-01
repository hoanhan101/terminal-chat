#!/usr/bin/env python3
"""
    Server.py - TCP Chat app server
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

class ServerThread(threading.Thread):

    def __init__(self, thread_id):

        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def listen(self):
        while True:
            s.listen(1)

            conn, addr = s.accept()
            CLIENTS[conn] = addr[0]

            print('Connection address: {0}'.format(addr[0]))

            data = conn.recv(BUFFER_SIZE).decode()
            sender = CLIENTS[conn]
            
            while data != "":
                print("Received \"{0}\" from IP {1}".format(data, sender))
                for client in CLIENTS:
                    message = '{0} : {1}'.format(sender, data)
                    client.send(message.encode())
                    print("Sent to {0}".format(CLIENTS[client]))
                data = conn.recv(BUFFER_SIZE).decode()
                #print("New data: {0}".format(data))

            conn.close()

        s.close()

    def run(self):
        print("Starting Thread {0}".format(self.thread_id))
        self.listen()
        print("Finishing Thread {0}".format(self.thread_id))


MAXIMUM_THREADS = 10
for i in range(MAXIMUM_THREADS):
    thread = ServerThread(i)
    thread.start()

#thread_1 = ServerThread(1)
#thread_2 = ServerThread(2)
#thread_3 = ServerThread(3)

#thread_1.start()
#thread_2.start()
#thread_3.start()

