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
mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# init a dictionary that stores client information in the format:
# {IP : [username, address_port]}
client_addresses = {}

online_clients = []
print('Server is now running...')

while True:
    # get data and address from the client
    data, addr = s.recvfrom(10240)
    data = data.decode()

    # init a message array that holds username and data
    message = []

    if data != '':
        if data[0] == '@':  # if data is username
            client_addresses[addr[0]] = [data]
            client_addresses[addr[0]].append(addr[1])
            online_clients.append(data)
            print('User {0} has connected from IP {1}.'.format(data,addr[0]))
            print('Current online clients: {0}'.format(online_clients))
            message = ['SERVER','{0} has joined the group chat from IP {1}.'.format(data,addr[0])]
        elif data == '/list':   # if data is /list command
            try:
                username = client_addresses[addr[0]][0]
                print('User {0} has requested a list of online clients.'.format(username))
                message = ['SERVER', 'A list of online clients: {0}'.format(online_clients)]
                s.sendto(pickle.dumps(message), addr)
            except KeyError:
                print('User doesn\'t exist...')
        elif data == '/help':   # if data is /help command
            message = ['SERVER', '/list : list online clients. /quit : exit chat app.']
            s.sendto(pickle.dumps(message), addr)
        else:   # if data is just message from client
            try:
                #print(client_addresses)
                username = client_addresses[addr[0]][0]
                print('Message from {0}: {1}'.format(username, data))
                client_addresses[addr[0]][1] = addr[1]
                if data != '/quit':
                    message = [username, data]
                else:
                    online_clients.remove(username)
                    print('User {0} has quit the group chat.'.format(username))
                    print('Current online clients: {0}'.format(online_clients))
                    message = ['SERVER', '{0} has quit the group chat.'.format(username)]
            except KeyError:
                print('User doesn\'t exist...')


        # bounce the message back to all clients, except the sender
        for IP in client_addresses:
            if IP == addr[0]:
                pass
            else:
                s.sendto(pickle.dumps(message), (IP, client_addresses[IP][1]))
