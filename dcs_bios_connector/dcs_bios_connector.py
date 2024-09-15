

from pyee import EventEmitter
from .control_parser import ControlParser
from .udp_listener import UdpListener
from .event_constants import NETWORK_DATA_MESSAGE


class DcsBiosConnector(EventEmitter):

    def __init__(self):
        super().__init__()
        self.updListener = UdpListener()
        self.control_parser = ControlParser()
    
        self.updListener.on(NETWORK_DATA_MESSAGE, self.control_parser.handle_incoming_dcs_bios_message)


    def connect(self):
        self.updListener.start()
    
    def send(self):
        print("not implemented yet")
