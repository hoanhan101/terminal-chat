#!/usr/bin/env python3
"""
    broad_cli2.py - UDP client that sends multicast messages on port 9000 and receives a message back.
    Author: Andrew Cencini (acencini@bennington.edu)
    Date: 9/17/2017
"""
import socket
import threading

MCAST_GRP = '224.0.0.1'  # which multicast group to talk to (https://en.wikipedia.org/wiki/Multicast_address)
			 # in this case, just all hosts on the local LAN segment
MCAST_PORT = 9000	 # UDP port to talk on

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class ClientThread(threading.Thread):
    def __init__(self, thread_id, function):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.function = function

    def send(self):
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

#client_addresses = {}
#
#while True:
#    MESSAGE = input(">> ")
#
#    # broadcast our message to the world
#    s.sendto(MESSAGE.encode(), (MCAST_GRP, MCAST_PORT))
#    print("SENT {0} TO {1}".format(MESSAGE, MCAST_GRP))
#
#    # now read back what we heard from the server
#    data, addr = s.recvfrom(1024)
#    
#    if addr[0] in client_addresses:
#        client_addresses[addr[0]] = addr[1]
#    else:
#        client_addresses[addr[0]] = addr[1]
#    
#    data = data.decode()
#    print("RECEIVED {0} FROM {1}".format(data, addr[0]))
