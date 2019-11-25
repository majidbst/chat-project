from threading import Thread
import threading

from server import *


# Simulates a socket instance
def xsocket(ip_proto, tcp_proto):
    if ip_proto != AF_INET or tcp_proto != SOCK_STREAM:
        raise Exception("Socket initiated with wrong values")
    return _stub


class socket:
    def __init__(self, ip_proto, tcp_proto):
        if ip_proto != AF_INET or tcp_proto != SOCK_STREAM:
            raise Exception("Socket initiated with wrong values")

    # --- Common methods
    def send(self, msg):
        _send_lock.acquire()
        _send_data.insert(0, msg)
        _send_lock.notify()
        _send_lock.release()
        print("Socket sending: {}".format(msg.decode()))

    def recv(self, length):
        # while len(self._data) < 1:
        _recv_lock.acquire()
        msg = b""
        while True:
            if _recv_data:
                msg = _recv_data.pop()
                break
            _recv_lock.wait()
        print("Socket received {}".format(msg))
        _recv_lock.release()
        return msg

    def close(self):
        print("Client close")

    # --- Server methods
    def bind(self, addr):
        if type(addr) != tuple:
            raise Exception("Socket bind with incorrect type")
        if len(addr) != 2:
            raise Exception("Socket bind with incorrect tuple length")
        # Store variable global to share it with the test client
        _server = addr

    def listen(self, count=0):
        return self

    def accept(self):
        _accept_lock.acquire()
        # _client[1] += 1
        return self, _client

    # --- Client methods
    def connect(self, addr):
        if addr[0] != _server[0] or addr[1] != _server[1]:
            raise Exception("Socket connect to incorrect server address or port")
        _client[1] += 1
        _accept_lock.release()
        return self


class test_stub(socket):
    # --- Common methods
    def send(self, msg):
        _recv_lock.acquire()
        _recv_data.insert(0, msg)
        _recv_lock.notify()
        _recv_lock.release()
        print("Test sending: {}".format(msg.decode()))

    def recv(self, length):
        _send_lock.acquire()
        msg = b""
        while True:
            if _send_data:
                msg = _send_data.pop()
                break
            _send_lock.wait()
        print("Socket received {}".format(msg))
        _send_lock.release()
        return msg

    def close(self):
        print("Test close")


# Public constants
AF_INET = 1
SOCK_STREAM = 2

#####    Global but private variables for the tests    ####

# Semaphores to lock the recv and accept methods
_recv_lock = threading.Condition()
_send_lock = threading.Condition()
_accept_lock = threading.Condition()
# Socket stub
# _stub = socket_stub()
# Internal data buffer list
_send_data = []
_recv_data = []
# Server and client socket data
_server = ("127.0.0.1", 12345)
_client = ["127.0.0.1", 75000]

