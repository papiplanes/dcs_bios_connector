from pyee import EventEmitter
from .control_parser import ControlParser
from .udp_connector import UDPConnector
from .event_constants import NETWORK_DATA_MESSAGE


class DcsBiosConnector(EventEmitter):

    def __init__(self):
        super().__init__()
        self.client = UDPConnector()
        self.control_parser = ControlParser(self)
    
        self.client.on(NETWORK_DATA_MESSAGE, self.control_parser.handle_incoming_dcs_bios_message)

    def connect(self):
        self.client.start()
    
    def send(self, message):
        self.client.send(message.strip() + '\n')
