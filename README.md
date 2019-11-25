# Chat application
A multi-threading client-server chat application for python course


# Requirements  
Python 3.4 or higher

## Modules:  
```
socket
threading
time
```

## Features:
- An object-oriented server code, but client code is procedural
- Implemented with AppJar GUI on client side
- It is a multi-threading program 
- Server starts by a thread which listening to incoming connections from
  clients and then issues a thread a in server for every client to
  handel receiving data from different clients
- All online clients collects into a dictionary by {conn:addr}
- Error and exception handling is implemented
- Non-blocking, deadlock prevention and reentrant lock implemented by 3
  semaphores

# Execution Instructions:
- to run the program, first run the chat_server.py
- secondly run client1.py, client2.py, ... for every instance 
of clients to simulate multi-threading

## Messaging protocol: 
(This protocol has not yet implemented)

A communication protocol which will implement on server and client, and
includes procedures to make the messages and distinguish different kind
of messages by parsing the massage string as:
- Broadcast
- Send to one specific client
- Send to a group of specified clients
- Sending clients list updates from server to all online clients

