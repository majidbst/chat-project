import unittest
import threading

from client1 import *

class TestMyFile(unittest.TestCase):

    def mtTest(self):
        lst = [1, 2, 3]
        expected_result = 6
        list_plus = sum_list(lst)

        self.assertEqual(list_plus, expected_result)




if __name__ == "__main__":
    unittest.main()


class TestMinFil(unittest.TestCase):
    def test_egen(self):


        self.assertEqual(value)






# --- Server test methods
class socket_test:
    def __init__(self, ip, port):
        print("Socket init")

    def bind(self, addr):
        print("Bind")

    def listen(self, count = 0):
        print("Listen")
        return self

    def accept(self):
        _accept_lock.acquire()
        #_client[1] += 1
        return self, _client

# --- Client test methods
def connect(self, addr):
    print("Connect")

def recv(self, length):
    _send_lock.acquire()
    msg = b""
    while True:
        if _send_data:



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
_recv_lock = []

_sever = ("127.0.0.1", 12345)
_client = ["127.0.0.1", 75000]
