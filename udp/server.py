#!/usr/bin/env python3
"""
    broad_serve2.py - UDP server that listens for multicast messages on port 9000 and prints them out and responds
                      to the sender with the message that was sent.
    Author: Andrew Cencini (acencini@bennington.edu)
    Date: 9/17/2017
"""
import socket
import struct

MCAST_GRP = '224.0.0.1'		# listen to all hosts on the local subnet
MCAST_PORT = 9000		# listen on UDP port 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# lets go of the socket after a crash
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind to all active network interfaces on the given UDP port
s.bind(('', MCAST_PORT))

# this is needed to set up the multicast group as an address to listen to
# we get the mcast address in network order (aton) - INADDR_ANY in this case
# just means listen on all local interfaces; we pack this into mreq so 
# we can listen to all callers
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    data, addr = s.recvfrom(10240)
    data = data.decode()
    print("{0} received: {1}".format(addr[0], data))

    # bounce the message back to the caller
    s.sendto(data.encode(), addr)
    print("Sent {0} to {1}".format(data, addr[0]))
