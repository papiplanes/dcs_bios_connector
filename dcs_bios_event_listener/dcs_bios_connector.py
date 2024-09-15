

from pyee import EventEmitter
from control_parser import ControlParser
from udp_listener import UdpListener


class DcsBiosEventListener(EventEmitter):

    def __init__(self):
        self.updListener = UdpListener()
        self.control_parser = ControlParser()
    
    def connect(self):
        self.updListener.start()
