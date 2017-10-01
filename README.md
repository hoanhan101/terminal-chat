# Group Chat Application

A simple group chat app.

# Design priciples
## TCP
### > Server
We set up a server to handle the mutiple requests using **Thread**. At the moment, the maximum threads are 10.
Whenever a request comes, a server does:
- accept the request
- add a client to a dictionary that holds the connection object and IP address
- send the message to all the clients in the dictionary

### > Client
Each client has two threads: one to send and one to receive.

## UDP
### > Server
We set up a server to listen to all connection.
Whenever a request comes, a server:
- get the data
- add the IP address of the connection, port and username to a dictionary
- send back the message to all clients in the dictionary

### > Client
Each client has two threads: one to send and one to receive

# How to test
For both TCP and UDP:
- Make sure all the machine you are testing are on the **same network**.
- Run the server file on **1 machine** and client file on **diffrent machines**.
- Follow the client file instruction.

# Errors
## TCP
- **OSError: [Errno 9] Bad file descriptor:** It happens when a client uses ^C to quit the chat.
- ~~**[errno 48] address already in use:** It happens because we don't close the socket properly.~~

# To-do
## TCP
- ~~Fix oserror: per permanently~~
- Open a new thread whenever a new connection ask for, custom thread number?, limit?
- Client have a custom username
- Nidesh DDoS acttack idea, "Around the World" one.

## UDP
- ~~UDP multicast~~
- ~~Login screen~~
- ~~Send a number with a message to keep the count and make sure all messages are delivered~~
- Error handling
- Curses module for seperate chat screen
- Special escape
- Add doc's requirements
