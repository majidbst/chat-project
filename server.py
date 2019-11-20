import socket
from threading import Thread
import threading
import queue
import time


clients = {}
connection_list = []

#local host IP '127.0.0.1
#host = 'localhost'
host = '127.0.0.1'
port = 8080
encoding = 'utf-8'

buffer_size = 2048
queue = queue.Queue()

lock = threading.RLock()


# Listen to new connections which are not already in connection_list
def listen():
    print('Listening thread starting for new connection.')
    while True:
        try:

            # Acquire a lock, blocking or non-blocking.
            lock.acquire()

            conn, addr = s.accept()
            print('Connected to: ', addr[0], ':', addr[1])

            # Set blocking or non-blocking mode of the socket: if flag is false, the socket is set to non-blocking, else to blocking mode.
            conn.setblocking(False)
            if conn not in connection_list:
                connection_list.append(conn)  # append the new connection to the list
        except socket.error:
            pass
        finally:
            # Release a lock, decrementing the recursion level.
            lock.release()
        time.sleep(0.050)

# Listen for new messages which all online clients send
def receive():
    print('Receiving thread starting to get new messages from clients')
    while True:
        if len(connection_list) > 0:
            for conn in connection_list:
                try:
                    # Acquire a lock, blocking or non-blocking.
                    lock.acquire()
                    data = conn.recv(buffer_size)
                except socket.error:
                    data = None
                finally:
                    # Release a lock, decrementing the recursion level.
                    lock.release()

            # checking data according to message protocol, to indicate massage type and other features
            analys_data(data, conn)


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
    for conn in clients:
        conn.send(data)

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

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    shutdown = False
    try:
        s.bind((str(host), int(port)))
        print("socket binded to port", port)

        # put the socket into listening mode
        s.listen(5)
        print("socket is listening...")

        # Set blocking or non-blocking mode of the socket:
        # if flag is 0, the socket is set to non-blocking, else to blocking mode.
        # Initially all sockets are in blocking mode.
        # In non-blocking mode, if a recv() call doesn’t find any data,
        # or if a send() call can’t immediately dispose of the data, an error exception is raised;
        # in blocking mode, the calls block until they can proceed.
        # s.setblocking(0) is equivalent to s.settimeout(0.0); s.setblocking(1) is equivalent to s.settimeout(None).
        s.setblocking(False)
    except socket.error:
        # close() releases the resource associated with a connection but does not necessarily close the connection immediately.
        # to close the connection in a timely fashion, call shutdown() before close()
        shutdown = True

    if not shutdown:

        #start 3 threads as
        listen_to_connections = Thread(target=listen, daemon=True)
        receive_messages = Thread(target=receive, daemon=True)
        send_messages = Thread(target=send, daemon=True)

        # Rlock class implements reentrant lock objects. A reentrant lock must be released by the thread that acquired it.
        # Once a thread has acquired a reentrant lock, the same thread may acquire it again without blocking;
        # the thread must release it once for each time it has acquired it.
     #   lock =  threading.RLock()


        listen_to_connections.start()
        receive_messages.start()
        send_messages.start()

    # Wait until threads terminates. This blocks the calling thread until the thread whose join() method is called terminates – either normally or through an unhandled exception – or until the optional timeout occurs.
  #  listen_to_connections.join()
 #   receive_messages.join()
  #  send_messages.join()

    # We never reach this line but it feels good to have it
    s.close()


"""
    If this file is called directly as a python program Main() will be called. 
    If it's included as a library nothing will be executed since all code is located in functions.
"""
if __name__ == '__main__':
    Main()

