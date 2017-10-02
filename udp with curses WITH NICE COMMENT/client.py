#!/usr/bin/env python3

"""
    client.py - UDP Chat app client
    Authors:
    - Hoanh An (hoanhan@bennington.edu)
    - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
    - Dung Le (dungle@bennington.edu)
    Date: 09/29/17
    Lastest Update: 10/1/17
"""

import socket
import threading
import pickle
import curses
from curses import wrapper
from ui import ChatUI

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# init UI screen
stdscr = curses.initscr()
curses.start_color()
ui = ChatUI(stdscr)

def send(stdscr):
    # add the welcome message to UI
    ui.chatbuffer_add('Welcome to our UDP chat!')
    # init an empty username string
    username = ''
    # continue if username is NOT NULL
    while True:
            try:
                username = ui.wait_input("Username: ")
                if not username:
                    raise ValueError("Username can't be NULL")
                else:
                    # send @ with username to notify the server it's the username
                    username = '@' + username
                    ui.chatbuffer.append(username)
                    ui.redraw_chatbuffer()
                    s.sendto(username.encode(), (MCAST_GRP, MCAST_PORT))
                    break
            except ValueError as e:
                print(e)
    
    # continuously read user input and send to the server
    while True:
        MESSAGE = ""
        while MESSAGE != "/quit":
            # read input from the UI
            MESSAGE = ui.wait_input()
            # broadcast our message to the world
            s.sendto(MESSAGE.encode(), (MCAST_GRP, MCAST_PORT))
            # add the message to the UI
            ui.chatbuffer_add('{0} : {1}'.format(username,MESSAGE))
        break

def receive(stdscr):
    while True:
        # get data and address from the server
        data, addr = s.recvfrom(1024)
        # load data into an array
        message_array = pickle.loads(data)
        sender = message_array[0]
        message = message_array[1]
        # send message to UI
        ui.chatbuffer_add('{0} : {1}'.format(sender,message))

"""
    Threading
"""

class ClientThread(threading.Thread):
    def __init__(self, thread_id, function):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.function = function

    def run(self):
        if self.function == "SEND":
            wrapper(send)
        elif self.function == "RECEIVE":
            wrapper(receive)

# creating new threads
thread_1 = ClientThread(1, "SEND")
thread_2 = ClientThread(2, "RECEIVE")

# set the RECEIVE thread to deamon
# so it can exit the program when SEND thread is done
thread_2.daemon = True

thread_1.start()
thread_2.start()
