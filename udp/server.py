#!/usr/bin/env python3

"""
    server.py - UDP Chat app server
    Authors:
    - Hoanh An (hoanhan@bennington.edu)
    - Nidesh Chitrakar (nideshchitrakar@bennington.edu)
    - Dung Le (dungle@bennington.edu)
    Date: 09/29/17
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

client_addresses = {}

while True:
    data, addr = s.recvfrom(10240)

    data = data.decode()
    message = []
    
    if data != "":
        if data[0] == '@':      # check if input string is username
            if bool(client_addresses) == False:      # if dictionary is empty
                client_addresses[addr[0]] = [data]
                client_addresses[addr[0]].append(addr[1])
                client_addresses[addr[0]].append(0)
                print('User {0} has connected from IP {1}.'.format(data,addr[0]))
                message = ['SERVER','{0} has joined the group chat.'.format(data)]
            else:       # dictionary is not empty
                # check if user exits in dictionary
                for client in client_addresses:
                    if data in client_addresses[client]:
                        print('user already exists!!!!1!')
                        message = ['SERVER','Username {0} already exists in the session. Please choose another username.'.format(data)]
                        s.sendto(pickle.dumps(message), addr)
                        break
                    else:
                        client_addresses[addr[0]] = [data]
                        client_addresses[addr[0]].append(addr[1])
                        client_addresses[addr[0]].append(0)
                        print('User {0} has connected from IP {1}.'.format(data,addr[0]))
                        print(client_addresses)
                        message = ['SERVER','{0} has joined the group chat.'.format(data)]
                        break
                    
#            for client in client_addresses:
#                if data in client_addresses[client]:
#                    print('user already exists!!!!1!')
#                    message = ['SERVER','Username {0} already exists in the session. Please choose another username.'.format(data)]
#
#                client_addresses[addr[0]] = [data]
#                client_addresses[addr[0]].append(addr[1])
#                client_addresses[addr[0]].append(0)
#                print('User {0} has connected from IP {1}.'.format(data,addr[0]))
#                message = ['SERVER','{0} has joined the group chat.'.format(data)]

        else:
            print(client_addresses)
            username = client_addresses[addr[0]][0]
            client_addresses[addr[0]][2] += 1

            print("FROM {0} MESSAGE #{1}: \"{2}\"".format(username, client_addresses[addr[0]][2], data))

            client_addresses[addr[0]][1] = addr[1]
            
            message = [username, data]
        # bounce the message back to the caller
        for IP in client_addresses:
            if IP == addr[0]:
                pass
            else:
                s.sendto(pickle.dumps(message), (IP, client_addresses[IP][1]))
                #print(" << {1} SENT {0} TO THE GROUP CHAT".format(data, username))


