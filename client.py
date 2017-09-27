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

TCP_ADDRESS = '127.0.0.1'

TCP_PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TCP_ADDRESS, TCP_PORT))

while True:
    MESSAGE = input("input: ")		# the message to send to the server
    s.send(MESSAGE.encode())
    print('Sent {0} to {1}'.format(MESSAGE, TCP_ADDRESS))

s.close()
