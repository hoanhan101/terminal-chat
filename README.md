# Group Chat Application

A simple group chat app.

## Design priciples
### Server
We set up a server to handle the mutiple requests using **Thread**. At the moment, the maximum threads are 10.
Whenever a request comes, server does:
- accept the request
- add a client to a dictionary that holds the connection object and IP address
- send the message to all the clients in the dictionary

### Client
Each client has two threads: one to send and one to receive.

## How to test

## Errors
- **OSError: [Errno 9] Bad file descriptor:** It happens when a client uses ^C to quit the chat.
- **[errno 48] address already in use:** It happens because we don't close the socket properly.
- ![I was blocked](images/i_was_blocked.png)

## To-do
- Open a new thread whenever a new connection ask for, custom thread number?, limit?
- Client have a custom username
- Fix oserror: per permanently
- How to test our chat app
- Nidesh DDoS acttack idea, "Around the World" one.
