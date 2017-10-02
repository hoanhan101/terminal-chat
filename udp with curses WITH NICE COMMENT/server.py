#!/usr/bin/env python3

"""
    server.py - UDP Chat app server
    Authors:
    - Hoanh An (hoanhan@bennington.edu)
    - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
    - Dung Le (dungle@bennington.edu)
    Date: 09/29/17
    Lastest Update: 10/1/17
"""

import socket
import struct
import pickle

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 9000

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

# init a dict that store client information in the format:
# {IP : [username, address_port, message_counter]}
client_addresses = {}
print('Server is now running')

# continously get requests
while True:
    # get the data and address from the client
    data, addr = s.recvfrom(10240)
    data = data.decode()
    
    # init a message array which holds username and data
    message = []
    
    # check if data is NULL
    if data != "":
        # if the data has @ in its first index, it has to be the username
        if data[0] == '@':
            # use the IP as the key in clients' dictionary
            client_addresses[addr[0]] = [data]
            # add the address port to the list
            client_addresses[addr[0]].append(addr[1])
            # add the message counter to the list, start with 0
            client_addresses[addr[0]].append(0)
            # prepare the message to send back to all client in the group
            message = ['SERVER','{0} has joined the group chat from IP {1}.'.format(data,addr[0])]
            print('User {0} has connected from IP {1}.'.format(data,addr[0]))

        else:
            try:
                username = client_addresses[addr[0]][0]
                # increase the message counter by 1
                client_addresses[addr[0]][2] += 1
                print("FROM {0} MESSAGE #{1}: \"{2}\"".format(username, client_addresses[addr[0]][2], data))
                # update the client address port
                client_addresses[addr[0]][1] = addr[1]
                if data != '/quit':
                    message = [username, data]
                else:
                    message = ['SERVER', '{0} has quit the group chat.'.format(username)]
            except KeyError:
                print("Username doesn't exist")

        # bounce the message back to all the clients, except the sender
        for IP in client_addresses:
            if IP == addr[0]:
                pass
            else:
                s.sendto(pickle.dumps(message), (IP, client_addresses[IP][1]))
