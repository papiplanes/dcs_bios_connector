import pkg_resources

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
            
            # Use pkg_resources to access files within the package
            resource_package = __name__  # Current package

            for file in pkg_resources.resource_listdir(resource_package, directory):
                if file.endswith('.json'):
                    # Get the path to the JSON file relative to the package
                    relative_path = os.path.join(directory, file)
                    json_file_paths.append(relative_path)
            print(json_file_paths)
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
            # Use pkg_resources to get the correct file path within the package
            json_path = pkg_resources.resource_filename('dcs_bios_connector', file)

            # Get the aircraft name from the filename (without extension)
            aircraft_name = os.path.basename(file).replace('.json', '')
            
            # Load JSON data
            with open(json_path, 'r') as f:
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