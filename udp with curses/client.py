#!/usr/bin/env python3

"""
    client.py - UDP Chat app client
    Authors:
    - Hoanh An (hoanhan@bennington.edu)
    - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
    - Dung Le (dungle@bennington.edu)
    Date: 09/29/17
"""

import socket
import threading

import pickle

from curses import wrapper
from ui import ChatUI

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# class ClientThread(threading.Thread):
#     def __init__(self, thread_id, function):
#         threading.Thread.__init__(self)
#         self.thread_id = thread_id
#         self.function = function

def send(stdscr):
    stdscr.clear()
    ui = ChatUI(stdscr)
    while True:
            try:
                #username = input('To get started, please provide a username: ')
                username = ui.wait_input("Username: ")
                if not username:
                    raise ValueError("Username can't be NULL")
                else:
                    username = '@' + username
                    ui.userlist.append(username)
                    ui.redraw_userlist()
                    s.sendto(username.encode(), (MCAST_GRP, MCAST_PORT))
                    break
            except ValueError as e:
                print(e)

    while True:
        #MESSAGE = input("{0}: ".format(username))
        MESSAGE = ""
        #while MESSAGE != "/quit":
        MESSAGE = ui.wait_input()
        ui.chatbuffer_add(MESSAGE)

            # broadcast our message to the world
        s.sendto(MESSAGE.encode(), (MCAST_GRP, MCAST_PORT))
            #print("SENT {0} TO {1}".format(MESSAGE, MCAST_GRP))

        data, addr = s.recvfrom(1024)
        #data = data.decode()
        #print("RECEIVED {0} FROM {1}".format(data, addr[0]))
        #print(data)
        messageArray = pickle.loads(data)
        sender = messageArray[0]
        message = messageArray[1]
        #print(' >> {0} : {1}'.format(sender,message))
        ui.userlist.append(sender)
        ui.redraw_userlist()
        ui.chatbuffer_add(message)
wrapper(send)

def receive(stdscr):
    while True:
        data, addr = s.recvfrom(1024)
        #data = data.decode()
        #print("RECEIVED {0} FROM {1}".format(data, addr[0]))
        #print(data)
        messageArray = pickle.loads(data)
        sender = messageArray[0]
        message = messageArray[1]
        #print(' >> {0} : {1}'.format(sender,message))
        ui.userlist.append(sender)
        ui.redraw_userlist()
        ui.chatbuffer_add(message)

#wrapper(receive)

    # def run(self):
    #     #print('Starting Thread {0}'.format(self.thread_id))
    #     print('Welcome to our UDP chat.')
    #
    #     if self.function == "SEND":
    #         self.send()
    #     elif self.function == "RECEIVE":
    #         self.receive()
    #
    #     print('Finishing Thread {0}'.format(self.thread_id))

# thread_1 = ClientThread(1, "RECEIVE")
# thread_2 = ClientThread(2, "SEND")
# thread_1.start()
# thread_2.start()
