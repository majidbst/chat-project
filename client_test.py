import unittest
import threading
import socket
from chat_server_oop import *
#from client1 import *

#Semaphores to lock the recv and accept methods
_recv_lock = threading.Condition()
_send_lock = threading.Condition()
_accept_lock = threading.Condition()


host = socket.gethostbyname(socket.gethostname())
port = 12345

class Test_setver(unittest.TestCase):

    def test_login(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port))

        login_msg = "Login" + ":" + "clientName"
        conn.sendall(login_msg.encode())
        rec = conn.recv(1024).decode()
        conn.close()
        self.assertEqual(rec, "Login:clientName")

    def test_broadcast(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port))

        msg = "msg" + ":" + "clientName" + ":" + "all" + ":" + "clientMessage"
        conn.sendall(msg.encode())
        rec = conn.recv(1024).decode()
        conn.close()
        self.assertEqual(rec, "clientName > clientMessage")

if __name__ == '__main__':
    unittest.main()



"""

    def test_server(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port))
        msg = "Hej"
        conn.send(msg.encode())
        rec = conn.recv(1024).decode()
        conn.close()
        #self.assertEqual(msg, rec[::-1])
        self.assertEqual(msg, rec)




class ClientTest(unittest.TestCase):

    def __init__(self):
        self.ip = server_ip
        self.port = server_port

    def run_fake_server(self):
        # Run a server to listen for a connection and then close it
        server_sock = socket.socket()
        server_sock.bind((self.ip, self.port))
        server_sock.listen(0)
        server_sock.accept()
        server_sock.close()

    def test_chat_client_connects_and_disconnects_to_default_server(self):
        # Start fake server in background thread
        server_thread = threading.Thread(target=self.run_fake_server)
        server_thread.start()

        # Test the clients basic connection and disconnection
        chat_client = client1.main()

        chat_client.connect(server_ip, server_port)
        chat_client.disconnect()

        # Ensure server thread ends
        server_thread.join()

    def connect(self, addr):
        print("Connect")

    def recv(self, length):
        _send_lock.acquire()
        msg = b""
        while True:
            if _send_data:
"""
