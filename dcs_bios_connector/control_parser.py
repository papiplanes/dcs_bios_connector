
import struct
from pyee import EventEmitter
from .aircraft_json_parser import AircraftJsonParser
from .parser import ProtocolParser


class ControlParser:
    def __init__(self, eventEmitterInstance):
        self.event_emitter = eventEmitterInstance
        self.aircraft_data, self.controls, self.address_lookup = AircraftJsonParser().get_aircraft_controls()
        self.emit_queue = []
        self.data_array =[0] * 65536
        self.string_controls = self._build_string_controls_index()
        self.parser = ProtocolParser(self.handle_data_change_for_address, self.handle_sync_complete)

    def handle_incoming_dcs_bios_message(self, message):
        for byte in bytearray(message):
            self.parser.process_byte(byte)

    def _build_string_controls_index(self):
        """
        Build a list of (start_address, control, output) tuples for every string
        output. The DCS-BIOS export protocol only transmits dirty 16-bit cells,
        so a string update can arrive at any cell inside the string's range
        (e.g. start + 2k), not necessarily at the string's start address.

        Sorting by start address lets us find the owning string for any address.
        """
        string_controls = []
        for control in self.controls.values():
            for output in control['outputs']:
                if output['type'] == 'string':
                    string_controls.append((output['address'], control, output))
        string_controls.sort(key=lambda item: item[0])
        return string_controls

    def _find_string_control(self, address):
        """
        Return the (control, output) of the string output whose range
        [start, start + max_length) contains the given address, or None.
        """
        for start_address, control, output in self.string_controls:
            if start_address <= address < start_address + output['max_length']:
                return control, output
        return None

    def _rebuild_string(self, output):
        """
        Rebuild the complete string from the byte-level memory image.

        Characters are stored one per byte, two per 16-bit cell (little-endian:
        low byte = character at addr, high byte = character at addr + 1), so the
        mirror holds consecutive characters at consecutive byte addresses
        starting at the string's start address. Partial updates may arrive at
        any cell inside the range; cells not yet received remain 0 (NULL) and
        are trimmed below along with space padding.
        """
        str_start = output['address']
        str_length = output['max_length']
        byte_data = bytes(self.data_array[str_start:str_start + str_length])
        text = byte_data.decode('utf-8', errors='replace')
        # Trim the NULL terminator and space padding
        return text.split('\x00', 1)[0].rstrip(' ')

    def parse_address_data(self,address, data):
        matching_outputs = []

        for control in self.address_lookup.get(address, []):
            for output in control['outputs']:
                if output['address'] == address:
                    matching_outputs.append((control, output))

        # A string update may arrive at any cell inside the string's range,
        # not just at its start address. Match against the range index too.
        if not matching_outputs:
            string_control = self._find_string_control(address)
            if string_control is not None:
                matching_outputs.append(string_control)

        for control, output in matching_outputs:
            if output['type'] == 'string':
                control_value = self._rebuild_string(output)
            else:
                control_value = (data & output['mask']) >> output['shift_by']

            value_has_changed = output.get('value') != control_value

            if value_has_changed:
                # Update the cached value. A string spans many 16-bit cells, so
                # one frame can deliver several write requests for the same
                # output; each one rebuilds the whole string. If the output is
                # already queued, just update its value (shared object) so the
                # latest rebuild is emitted at sync, otherwise queue it once.
                output['value'] = control_value
                if not any(item['output'] is output for item in self.emit_queue):
                    self.emit_queue.append({'output': output, 'control': control})

    def handle_data_change_for_address(self, address, data):
        bytes_data = struct.pack('<H', data)
        self.data_array[address] = bytes_data[0]
        self.data_array[address + 1] =  bytes_data[1]
        self.parse_address_data(address, data)

    def handle_sync_complete(self):
        for item in self.emit_queue:
            identifier = item['control']['identifier'] + item['output']['suffix']
            self.event_emitter.emit(identifier, item['output']['value'], item['control'], item['output'])
            self.event_emitter.emit(identifier + ':' + str(item['output']['value']))
        self.emit_queue = []
