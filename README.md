# GROUP CHAT APP

## UDP DESIGN
### SERVER
We set up the server that listen to all the connections. Whenever a request comes, a server first get the data and address. Since in the client side, we set the first message sent by the client is his/her username. We use that data to store the username in a dictionary as the format: `{IP : [username, address_port, message_count]}`

Each time the **same** client login, he/she has the same IP but different port. We save the address port so we can update it constantly. The message count is used to count the message received of each client. It increases by 1 everytime the client send a new message. In the future, we can use that sequential proof to prevent data loss.

Now we have the username from the first message, so from the second message, we only received data from the client. We save that data in an array which holds the username and data. We know username of the sender, so we don't have to use the IP as an indentifier.

In the end, we use the client's dictionary to notify everyone in the group chat.

### CLIENT
Each client have 2 threads: one to send and one to receive. 

For the send thread, as we implemented the login interface, the first thing each client send to the server is his/her own username. We put a try except block here to make sure that the username will not be NULL. Otherwise, send the username or the message to the server.

For the receive thread, we retrieved the data (an array containing the username and his/her corresponding message) using pickle, and displayed it on the screen.


## TO-DO
- ~~UDP multicast~~
- ~~Login screen~~
- ~~Send a number with a message to keep the count and make sure all messages are delivered~~
- ~~Curses module for seperate chat screen~~
- The client terminal messed up when using ^C to quit instead of /quit
- The cursor keeps jumping to the message that you sent
- How to delete user from dict when one quits
- Print out the list of online user
- How to do without threading? Message queue?

## TESTING
- Make sure all the machine you are testing are on the **same network**.
- Run the server file on **1 machine** and client file on **diffrent machines**.
- Follow the client file instruction.

---

## TCP DESIGN

### SERVER
We set up a server to handle the mutiple requests using **Thread**. At the moment, we have a fixed number of threads equals to 10. Each client has his/her own thread so our server can only handle maximum 10 clients. We will look for better solution in our freetime since our UDP chat app is our main focus at the moment.

Back to our design priciples, when a request comes, a server get connection and address. We save the connection object and IP from the address in a dictionary as the format `{ConnectionObject : IP}`.  We get the data from the connection object and send back to all the client in that dictionary.

### CLIENT
Each client have 2 threads: one to send and one to receive.


## TO-DO
- **OSError: [Errno 9] Bad file descriptor:** It happens when a client uses ^C to quit the chat.
- **[errno 48] address already in use:** It happens because we don't close the socket properly.
- Open a new thread whenever a new connection ask for, custom thread number?, limit?


