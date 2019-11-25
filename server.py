import socket
from threading import Thread
import threading
import queue
import time

host = 'localhost'
port = 12378
encoding = 'utf-8'


clients = {}           # dictionary of all clients by conn and addr
connection_list = []   # list of all sockets which server listening and receiving data to/from them
login_list = []
receive_messages_thread = []


buffer_size = 1024
queue = queue.Queue()

# A reentrant lock is a synchronization primitive that may be acquired multiple times by the same thread
#A reentrant lock must be released by the thread that acquired it. Once a thread has acquired a reentrant lock, the same thread may acquire it again without blocking; the thread must release it once for each time it has acquired it.
_recv_lock = threading.RLock()
_send_lock = threading.RLock()
_accept_lock = threading.RLock()

def handle_client(conn):
    print('Receiving thread starting to get new messages from clients')
    print("Connection_list: ", connection_list)
    while True:
        if len(connection_list) > 0:
            for conn in connection_list:
                try:
                    """Acquire a lock, blocking or non-blocking."""
                    _recv_lock.acquire()
                    data = conn.recv(buffer_size)
                except socket.error:
                    data = None
                finally:
                    """Release a lock, decrementing the recursion level."""
                    _recv_lock.release()

            """checking data according to message protocol, to indicate massage type and other features"""
            analys_data(data, conn)


"""Send messages from server's queue"""
def send():
    print('Send started')


"""Send message to a specified client"""
def send_to_one(destination, data):
    print("Send message to a specified client", destination)
    target_address = login_list[destination]
    try:
        _send_lock.acquire()
        target_address.send(data)
    except socket.error:
        remove_connection(target_address)
    finally:
        _send_lock.release()

"""Send message to a selected list of clients"""
def send_to_selected_clients(destination_list, data):
    print("Send message to selected clients")


"""broadcast data to all clients"""
def broadcast(data):
    print("Broadcast message ...")

    for conn in clients:
        try:
            _send_lock.acquire()
            conn.send(data)
            print("Sending data to: ", conn)
        except socket.error:
            print("No client")
        finally:
            _send_lock.release()

"""Remove connection from server's connection list"""
def remove_connection(connection):
    connection_list.remove(connection)
    for login, address in login_list:
        if address == connection:
            del login_list[login]
            break
    update_login_list()

"""receive function"""
def receive(conn):
    while True:
        """data received from client"""
        data = conn.recv(buffer_size)
        if not data:
            print('Bye')
            break
        if data == b"quit":
            print("Client quit")
            conn.send(data)
            break

        #analys_data(data, conn)

        """send message to all clients"""
        broadcast(data)

    """remove a closed client from the client dictionary"""
    del (clients[conn])

# Check received data from clients according to communication protocol to indicate message type and other delivery options

# communication protocol:
    # template:
    # client1 sends message to client2:
    # client sends message to all clients:
    # client login or logout:
    # server to clients notifications when login list changes:

"""this function not completed"""
def analys_data(data, conn):
    if data:
        msg = data.decode(encoding)
        print("Message: ", msg)

"""Update list of online clients"""
def update_client_list():
    print("This function not completed")

"""remove closed clients from the clients list"""
def delete_client(conn):
    connection_list.remove(conn)
    for client, addr in clients.items():
        if addr == conn:
            del clients[client]
            break
    update_client_list()


def Main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((str(host), int(port)))
        print("socket binded to port", port)
        s.listen(5)
        print("socket is listening...")
    except socket.error:
        print("socket error.")

    while True:
        try:
            """Acquire a lock, blocking or non-blocking."""
            _recv_lock.acquire()

            conn, addr = s.accept()
            print("Connected to Conn: ", conn)
            print("%s:%s socket has connected to the client." % addr)
            conn.send(b"Welcome to chat!")

            """Set blocking or non-blocking mode of the socket"""
            #conn.setblocking(False)
            if conn not in clients:
                """Dictionary of client addresses with socket with conn as key and addr as value"""
                clients[conn] = addr
                #connection_list.append(conn)
                print("New connection was added to the connection_list.")
                #broadcast(conn, "\n[%s:%s] entered the chat room\n" % addr)


                """this thread do just broadcasting"""
                client_thread = Thread(target=receive, args=(conn,))
                receive_messages_thread.append(client_thread)

                """this thread handle all communications as one-to-one/one-to-many, but but final yet"""
                # receive_messages_thread = Thread(target=handle_client, args=(conn,), daemon=True)
                #receive_messages_thread.start()
                client_thread.start()

        except socket.error:
            print("Server socket error.")
        finally:
            """Release a lock, decrementing the recursion level."""
            _recv_lock.release()
            time.sleep(0.050)

    for thrd in receive_messages_thread:
        thrd.join()
    s.close()

if __name__ == '__main__':
    Main()

