from pyee import EventEmitter

import socket
import struct
import threading
from .event_constants import NETWORK_DATA_MESSAGE

MULTICAST_GROUP = '239.255.50.10'
PORT = 5010
LOOPBACK_INTERFACE  = ""

class UdpListener(EventEmitter):
    def __init__(self):
        super().__init__()

    def udp_listener(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((LOOPBACK_INTERFACE, PORT))

        mreq = struct.pack('4sl', socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        print(f"Listening for data on {MULTICAST_GROUP}:{PORT}...")

        while True:
            data, addr = sock.recvfrom(65536)  # Buffer size of 65536 bytes
            self.emit(NETWORK_DATA_MESSAGE, data)

    def start(self):
        self.thread = threading.Thread(target=self.udp_listener)
        self.thread.daemon = True  # Makes sure the thread exits when the main program does
        self.thread.start()