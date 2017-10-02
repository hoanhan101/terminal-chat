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

import curses
from curses import wrapper
from ui import ChatUI

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

stdscr = curses.initscr()
curses.start_color()
ui = ChatUI(stdscr)

def send(stdscr):
    ui.chatbuffer_add('Welcome to our UDP chat.')
    username = ''
    while True:
            try:
                username = ui.wait_input("Username: ")
                if not username:
                    raise ValueError("Username can't be NULL")
                else:
                    username = '@' + username
                    ui.chatbuffer.append(username)
                    ui.redraw_chatbuffer()
                    s.sendto(username.encode(), (MCAST_GRP, MCAST_PORT))
                    break
            except ValueError as e:
                print(e)

    while True:
        MESSAGE = ""
        while MESSAGE != "/quit":
            MESSAGE = ui.wait_input()

            # broadcast our message to the world
            s.sendto(MESSAGE.encode(), (MCAST_GRP, MCAST_PORT))
            #print("SENT {0} TO {1}".format(MESSAGE, MCAST_GRP))
            ui.chatbuffer_add(' << {0} : {1}'.format(username,MESSAGE))
        break

def receive(stdscr):
    #ui = ChatUI(stdscr)
    while True:
        data, addr = s.recvfrom(1024)
        messageArray = pickle.loads(data)
        sender = messageArray[0]
        message = messageArray[1]
        if sender == 'SERVER' and message == '/quit':
            break
        else:
            ui.chatbuffer_add(' >> {0} : {1}'.format(sender,message))
"""
    Threading
"""
class ClientThread(threading.Thread):
    def __init__(self, thread_id, function):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.function = function


    def run(self):
        #print('Starting Thread {0}'.format(self.thread_id))
        #print('Welcome to our UDP chat.')

        if self.function == "SEND":
            wrapper(send)
            #self.send()
        elif self.function == "RECEIVE":
            wrapper(receive)
            #self.receive()

        print('Finishing Thread {0}'.format(self.thread_id))

threads = []

# creating new threads
thread_1 = ClientThread(1, "SEND")
thread_2 = ClientThread(2, "RECEIVE")

# starting the threads
thread_1.start()
thread_2.start()

# add the threads to the thread list
threads.append(thread_1)
threads.append(thread_2)

# wait for all threads to complete
# for thread in threads:
#     thread.join()
