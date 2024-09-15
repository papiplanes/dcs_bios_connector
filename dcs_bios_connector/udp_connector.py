from pyee import EventEmitter
import socket
import struct
import threading
from .event_constants import NETWORK_DATA_MESSAGE

MULTICAST_GROUP = '239.255.50.10'
PORT = 5010
SEND_PORT = 7778
LOOPBACK_INTERFACE = ""

class UDPConnector(EventEmitter):
    def __init__(self):
        super().__init__()
        
        # Setup listening socket
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_sock.bind((LOOPBACK_INTERFACE, PORT))

        mreq = struct.pack('4sl', socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
        self.listen_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Setup sending socket
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    def udp_listener(self):
        while True:
            data, addr = self.listen_sock.recvfrom(65536)  # Buffer size of 65536 bytes
            self.emit(NETWORK_DATA_MESSAGE, data)

    def start(self):
        self.thread = threading.Thread(target=self.udp_listener)
        self.thread.daemon = True  # Makes sure the thread exits when the main program does
        self.thread.start()

    def send(self, message):
        self.send_sock.sendto(message.encode('utf-8'), ('127.0.0.1', SEND_PORT))

    def close(self):
        """
        Close both the listening and sending sockets.
        """
        self.listen_sock.close()
        self.send_sock.close()
