#!/usr/bin/env python3
"""
    broad_cli2.py - UDP client that sends multicast messages on port 9000 and receives a message back.
    Author: Andrew Cencini (acencini@bennington.edu)
    Date: 9/17/2017
"""
import socket

MCAST_GRP = '224.0.0.1'  # which multicast group to talk to (https://en.wikipedia.org/wiki/Multicast_address)
			 # in this case, just all hosts on the local LAN segment
MCAST_PORT = 9000	 # UDP port to talk on
MESSAGE = "Hello World!!"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# broadcast our message to the world
s.sendto(MESSAGE.encode(), (MCAST_GRP, MCAST_PORT))
print("Sent {0} to {1}".format(MESSAGE, MCAST_GRP))

# now read back what we heard from the server
data, addr = s.recvfrom(1024)
data = data.decode()
print("{0} received {1}".format(addr[0], data))
