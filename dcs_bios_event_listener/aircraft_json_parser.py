import os
import json

class AircraftJsonParser:
    def __init__(self):
        self.directory = './json'
        self.files = self.get_json_file_paths(self.directory)
    
    def get_aircraft_controls(self):
        return  JsonParser().parse_files(self.files)

    def get_json_file_paths(self, directory):
            """
            Get a list of relative paths to JSON files under the specified directory.

            :param directory: The directory to search for JSON files.
            :return: A list of relative paths to JSON files.
            """
            json_file_paths = []
            
            # Traverse the directory
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.json'):
                        # Get the absolute path to the JSON file
                        absolute_path = os.path.join(root, file)
                        json_file_paths.append(absolute_path)
            
            return json_file_paths


class JsonParser:
    @staticmethod
    def parse_files(files, aircraft_data=None, controls=None, address_lookup=None):
        if aircraft_data is None:
            aircraft_data = {}
        if controls is None:
            controls = {}
        if address_lookup is None:
            address_lookup = {}

        for file in files:
            # Get the aircraft name from the filename (without extension)
            aircraft_name = os.path.basename(file).replace('.json', '')
            
            # Load JSON data
            with open(file, 'r') as f:
                json_data = json.load(f)
            
            aircraft_data[aircraft_name] = json_data

            # Parse the aircraft's controls
            JsonParser._parse_json(json_data, controls, address_lookup)

        return aircraft_data, controls, address_lookup

    @staticmethod
    def _parse_json(json_data, controls, address_lookup):
        # Aircraft data is structured as Category -> [Array of Controls] -> [Array of Outputs]. We need to go 2 levels deep
        # to get the outputs.
        for category in JsonParser._get_values(json_data):
            for control in JsonParser._get_values(category):
                controls[control['identifier']] = control

                # Get the outputs for each control and add them to the address lookup
                for output in control['outputs']:
                    # Create the list at the control's address if it doesn't exist
                    if output['address'] not in address_lookup:
                        address_lookup[output['address']] = []
                    address_lookup[output['address']].append(control)

    @staticmethod
    def _get_values(obj):
        # In Python 3, we can use the .values() method directly
        if isinstance(obj, dict):
            return list(obj.values())
        else:
            return []