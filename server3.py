import socket
from threading import Thread
import threading
import queue
import time


clients = {}           # dictionary of all clients by conn and addr
#connection_list = []   # list of all sockets which server listening and receiving data to/from them
connection_list = []

#local host IP '127.0.0.1
host = 'localhost'
port = 8088
encoding = 'utf-8'

buffer_size = 2048
queue = queue.Queue()

# A reentrant lock is a synchronization primitive that may be acquired multiple times by the same thread
#A reentrant lock must be released by the thread that acquired it. Once a thread has acquired a reentrant lock, the same thread may acquire it again without blocking; the thread must release it once for each time it has acquired it.
_recv_lock = threading.RLock()
_send_lock = threading.RLock()
_accept_lock = threading.RLock()

"""
# Semaphores to lock the receive, send and accept methods
_recv_lock = threading.Condition()
_send_lock = threading.Condition()
_accept_lock = threading.Condition()
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# shutdown = False
try:
    s.bind((str(host), int(port)))
    print("socket binded to port", port)
    s.listen(5)
    print("socket is listening...")
except socket.error:
    print("socket error.")


def handle_client(conn, addr):
    print('Receiving thread starting to get new messages from clients')
    while True:
        if len(connection_list) > 0:
            for conn in connection_list:
                try:
                    # Acquire a lock, blocking or non-blocking.
                    _recv_lock.acquire()
                    data = conn.recv(buffer_size)
                except socket.error:
                    data = None
                finally:
                    # Release a lock, decrementing the recursion level.
                    _recv_lock.release()

            # checking data according to message protocol, to indicate massage type and other features

            #analys_data(data, conn)


# Send messages from server's queue
def send():
    print('Sender thread started')

# Send message to all clients except source clients
def send_to_all(source, data):
    print("Send message to all clients except sender client")


# Send message to a specified client
def send_to_one(destination, data):
    print("Send message to a specified client")


# Send message to a selected list of clients
def send_to_selected_clients(destination_list, data):
    print("Send message to selected clients")


# broadcast data to all clients
def broadcast(data):
    print("Broacast message")
    for conn in connection_list:
        try:
            _send_lock.acquire()
            conn.send(data)
            print("Sending data to: ", conn)
        except socket.error:
            print("No client")

        finally:
            _send_lock.release()


"""
# receive function
def receive(c):
    while True:

        # data received from client
        data = c.recv(buffer_size)
        if not data:
            print('Bye')
            # lock released on exit
            #print_lock.release()
            break
        if data == b"quit":
            print("Client quit")
            c.send(data)
            break

        # send message to all clients
        broadcast(data)
    # c.close()

    # remove a closed client from the client dictionary
    del (clients[c])
"""

# Check received data from clients according to communication protocol to indicate message type and other delivery options

# communication protocol:
    # template: "action_type;source;destination;message"
    # client1 sends message to client2: "msg;user1;user2;message"
    # user sends message to all users: "msg;user;ALL;message"
    # user logs in or out: "login;user" / "logout;user"
    # notification from server to clients on login list changes: "login;client1;client2;client3;[...];ALL"
def analys_data(data, conn):
    if data:
        msg = data.decode(encoding)
        msg = msg.split(";", 3)

        if msg[0] == 'login':
            clients[msg[1]] = conn
            print(msg[1] + ' has logged in')
            update_client_list()

        elif msg[0] == 'logout':
            connection_list.remove(clients[msg[1]])
            print(msg[1] + ' has logged out')
            update_client_list()

        elif msg[0] == 'msg' and msg[2] != 'all':
            msg = data.decode(encoding) + '\n'
            data = msg.encode(encoding)
            queue.put((msg[2], msg[1], data))

        elif msg[0] == 'msg':
            msg = data.decode(encoding) + '\n'
            data = msg.encode(encoding)
            queue.put(('all', msg[1], data))

# Update list of online clients"""
def update_client_list():
    print("This function not completed")

# Delete connection from connection list
# to remove closed clients from the clients list
def delete_client(conn):
    connection_list.remove(conn)
    for client, addr in clients.items():
        if addr == conn:
            del clients[client]
            break
    update_client_list()


def Main():



    while True:
        try:
            # Acquire a lock, blocking or non-blocking.
            _recv_lock.acquire()

            conn, addr = s.accept()
            print("Connected to Conn: ", conn)
            # print('Connected to: ', addr[0], ':', addr[1])
            print("Client %s:%s has connected." % addr)

            # Set blocking or non-blocking mode of the socket: if flag is false, the socket is set to non-blocking, else to blocking mode.
            # if flag is 0, the socket is set to non-blocking, else to blocking mode.
            # Initially all sockets are in blocking mode.
            # In non-blocking mode, if a recv() call doesn’t find any data,
            # or if a send() call can’t immediately dispose of the data, an error exception is raised;
            # in blocking mode, the calls block until they can proceed.
            # s.setblocking(0) is equivalent to s.settimeout(0.0); s.setblocking(1) is equivalent to s.settimeout(None).
            conn.setblocking(False)
            if conn not in connection_list:
                # Dictionary of client addresses with socket with conn as key and addr as value
                connection_list.append(conn)
                print("New connection was added to the connection_list.")

                receive_messages_thread = Thread(target=handle_client, args=(conn,), daemon=True)
                receive_messages_thread.start()

        except socket.error:
            pass
        finally:
            # Release a lock, decrementing the recursion level.
            _recv_lock.release()
        time.sleep(0.050)

    # for thrd in connection_list:
    #     thrd.join()


    # We never reach this line but it feels good to have it
    s.close()

"""
    If this file is called directly as a python program Main() will be called. 
    If it's included as a library nothing will be executed since all code is located in functions.
"""
if __name__ == '__main__':
    Main()

