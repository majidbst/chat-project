import socket
from threading import Thread
import threading
import time

#host = 'localhost'
host = socket.gethostbyname(socket.gethostname())
port = 12345
encoding = 'utf-8'

class ChatServer(threading.Thread):
    def __init__(self, host, port):
        super().__init__(daemon=False, target=self.run)

        """chat server initialization"""
        self.host = host
        self.port = port
        self.buffer_size = 1024
        self.clients = {}              # put all online clients into a dict
        self.server_is_running = True  # check is server is on
        self.receive_messages_thread = []

        """A reentrant lock is a synchronization primitive that may be acquired multiple times by the same thread"""
        self._recv_lock = threading.RLock()
        self._send_lock = threading.RLock()
        self._accept_lock = threading.RLock()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.bind((str(host), int(port)))
            print("host: ", host)
            print("socket binded to port", port)
            self.s.listen(5)
            print("socket is listening...")

        except socket.error:
            self.server_is_running = False
            print("socket error.")

        if self.server_is_running == True:
            self.listen_to_new_conn()
            self.start()

    """Main thread method which waits to get quit command from user to end the chat server"""
    def run(self):
        print("To exit the chat server enter \'q\'")
        while self.server_is_running:
            message = input("Waiting for quit command: ")
            if message == 'q':
                self.s.close()
                self.server_is_running = False

    """Listen to new connections"""
    def listen_to_new_conn(self):
        while self.server_is_running:
            try:
                self._accept_lock.acquire()
                conn, addr = self.s.accept()
                conn.setblocking(False)      #Set to non-blocking mode of the socket. Initially all sockets are in blocking mode.
                if conn not in self.clients:
                    self.clients[conn] = addr
                    print("New connection was added to the clients dict.")
                    #self.broadcast("\n[%s:%s] entered to the chat room\n" % addr)

                    client_thread = Thread(target=self.receive, args=(conn,), daemon=True)  # thread that receive data from client
                    self.receive_messages_thread.append(client_thread)  # collect receiving threads from every client
                    client_thread.start()

            except socket.error:
                pass
            finally:
                self._accept_lock.release()
            time.sleep(0.050)


    """receive function"""
    def receive(self, conn):
        print('Receive thread initiated.')
        while True:
            if len(self.clients) > 0:
                for client in self.clients:
                    try:
                        self._recv_lock.acquire()
                        data = client.recv(self.buffer_size)
                    except socket.error:
                        data = None
                    finally:
                        self._recv_lock.release()

                    self.analys_data(data, conn)


    """broadcast data to all clients"""
    def broadcast(self, data):
        print("Broadcast message ...")
        for conn in self.clients:
            try:
                self._send_lock.acquire()
                conn.send(data)
                print("Sending data to: ", conn)
            except socket.error:
                print("No client")
            finally:
                self._send_lock.release()


    """analys receiving data and do the further action according to the message protocol"""
    def analys_data(self, data, conn):
        if data:
            #msg = data.decode(encoding)
            self.broadcast(data)


    """Send message to a specified client"""
    def send_to_one_client(self, conn, data):
        print("Send message to a specified client", conn)
        target_address = self.clients[conn]
        try:
            self._send_lock.acquire()
            target_address.send(data)
        except socket.error:
            remove_connection(target_address)
        finally:
            self._send_lock.release()

    """Send message to a selected list of clients"""
    def send_to_selected_clients(self, destination_list, data):
        print("Send message to selected clients")
        for conn in destination_list:
            try:
                self._send_lock.acquire()
                conn.send(data)
            except socket.error:
                self.delete_connection(target_address)
            finally:
                self._send_lock.release()

    """Delete connection from connection list"""
    def delete_connection(self, conn):
        for client, addr in self.clients.items():
            if addr == conn:
                del self.clients[client]
                break
        self.update_clients()

    """update online clients list"""
    def update_clients():
        print("This function not completed")

"""instantiate a server"""
if __name__ == '__main__':
    chatServer = ChatServer(host, port)

