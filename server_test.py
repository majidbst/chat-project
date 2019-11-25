import unittest
import socket
import threading

from server import *


# public constants
AF_INET = 1
SOCK_STREAM = 2


# Global but private variables for the test

#Semaphores to lock the recv and accept methods
_recv_lock = threading.Condition()
_send_lock = threading.Condition()
_accept_lock = threading.Condition()

# internal data buffer lists
_send_data = []
_recv_data = []

_sever = ("127.0.0.1", 12345)
_client = ["127.0.0.1", 75000]

server_ip = "127.0.0.1"
server_port = 12345

"""--- Server test methods"""
class SocketTest(unittest.TestCase):

    def __init__(self):
        self.ip = server_ip
        self.port = server_port

    def test_chat_server_start(self):

        chat_server = server.main()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(self.ip, self.port)
        s.listen(5)

        server_thread = threading.Thread(target=chat_server)
        server_thread.start()


        # On my computer, 0.0000001 is the minimum sleep time or the
        # client might connect before server thread binds and listens
        # Other computers will differ. I wanted a low number to make tests fast
        time.sleep(0.000001)

        # This is our fake test client that is just going to attempt a connect and disconnect
        fake_client = socket.socket()
        fake_client.settimeout(1)
        fake_client.connect((self.ip, self.port))
        fake_client.close()

        # Make sure server thread finishes
        server_thread.join()

    def bind(self, addr):
        print("Bind")

    def listen(self, count=0):
        print("Listen")
        return self

    def accept(self):
        _accept_lock.acquire()
        # _client[1] += 1
        return self, _client


