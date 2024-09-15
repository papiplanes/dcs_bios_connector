
import struct
from pyee import EventEmitter
from .aircraft_json_parser import AircraftJsonParser
from .parser import ProtocolParser


class ControlParser(EventEmitter):
    def __init__(self):
        super().__init__()
        self.aircraft_data, self.controls, self.address_lookup = AircraftJsonParser().get_aircraft_controls()
        self.emit_queue = []
        self.data_array =[0] * 65536
        self.parser = ProtocolParser(self.handle_data_change_for_address, self.handle_sync_complete)

    def handle_incoming_dcs_bios_message(self, message):
        for byte in bytearray(message):
            self.parser.process_byte(byte)

    def parse_address_data(self,address, data):
        if address not in self.address_lookup:
            return
        
        for control in self.address_lookup[address]:
            for output in control['outputs']:
                if output['address'] == address:
                    if output['type'] == 'string':
                        data_values = self.data_array[address:address + output['max_length']]

                        byte_data = bytes(data_values)
                        utf8_string = byte_data.decode('utf-8')
                        control_value = utf8_string
                    else:
                        control_value = (data & output['mask']) >> output['shift_by']
                    
                    value_has_changed = output.get('value') != control_value
                    is_already_added = any(item['control'] == control and item['output'] == output for item in self.emit_queue)

                    if value_has_changed and not is_already_added:
                        output['value'] = control_value
                        self.emit_queue.append({'output': output, 'control': control})

    def handle_data_change_for_address(self, address, data):
        bytes_data = struct.pack('<H', data)
        self.data_array[address] = bytes_data[0]
        self.data_array[address + 1] =  bytes_data[1]
        self.parse_address_data(address, data)

    def handle_sync_complete(self):
        for item in self.emit_queue:
            identifier = item['control']['identifier'] + item['output']['suffix']
            self.emit(identifier, item.output.value, item.control, item.output)
            self.emit(identifier + ':' + item.output.value, item.control, item.output)
        self.emit_queue = []
