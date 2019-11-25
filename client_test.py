import unittest
from client1 import *


server_ip = "127.0.0.1"
server_port = 12345

#Semaphores to lock the recv and accept methods
_recv_lock = threading.Condition()
_send_lock = threading.Condition()
_accept_lock = threading.Condition()


"""--- Client test methods"""
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

